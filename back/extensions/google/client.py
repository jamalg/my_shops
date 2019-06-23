from typing import Dict, Optional, List
import urllib
import json

import requests

from back.config import config
from back.utils.geo import Coordinates
from back.utils.image import Image
from back.extensions.google import constants
from back.extensions.google.exceptions import GoogleApiError
from back.extensions.google.mixins import ExcecutorMixin, PhotoApiMixin
from back.extensions.google.caching import redis_cache


class GoogleCloudApi(ExcecutorMixin, PhotoApiMixin):
    def __init__(self, api_key: str = None, output: str = "json") -> None:
        self.output = output
        self.api_key = api_key

    def _get(self, url: str, params: Dict) -> Dict:
        url_params = urllib.parse.urlencode(params, safe=",")
        response = requests.get("{}?{}".format(url, url_params))
        if response.ok:
            data = response.json()
            if data["status"] in constants.GOOGLE_PLACES_OK_STATUSES:
                return data
            raise GoogleApiError(message=data.get("error_message", data["status"]), data=data)
        raise GoogleApiError.from_http_response(response)

    @redis_cache(expiry=config.PHOTO_TTL, serialize=Image.serialize, deserialize=Image.deserialize)
    # Granted that Redis is not the best solution for image caching. As this can very quickly eat up memory
    # But we restricted the image size in configuration to mitigate
    def photo(
            self,
            *,
            photo_reference: str,
            max_height: Optional[int] = None,
            max_width: Optional[int] = None
            ) -> Image:
        params = dict(
            key=self.api_key,
            photoreference=photo_reference,
        )
        if max_height is not None and max_width is None:
            params["maxheight"] = max_height
        elif max_height is None and max_width is not None:
            params["maxwidth"] = max_width
        else:
            raise GoogleApiError(message="Exclusively supply either max_height or max_width")

        url_params = urllib.parse.urlencode(params)
        response = requests.get("{}?{}".format(constants.GOOGLE_PLACE_PHOTO_URL, url_params))
        if response.ok:
            metadata = GoogleCloudApi.headers_to_photo_metadata(response.headers)
            return Image(
                binary=response.content,
                mimetype=metadata["mimetype"],
                filename=metadata["filename"]
            )
        raise GoogleApiError.from_http_response(response)

    @redis_cache(expiry=config.NEARBY_PLACE_TTL, serialize=lambda o: json.dumps(o), deserialize=lambda o: json.loads(o))
    def nearby(self, *, location: Coordinates, radius: int, type: str) -> Dict:
        params = dict(
            key=self.api_key,
            location=str(location),
            radius=radius,
            type=type
        )
        url = "{}/{}".format(constants.GOOGLE_PLACES_NEARBY_URL, self.output)
        return self._get(url=url, params=params)["results"]

    @redis_cache(expiry=config.PLACE_TTL, serialize=lambda o: json.dumps(o), deserialize=lambda o: json.loads(o))
    def place(self, *, place_id: str) -> Dict:
        params = dict(
            key=self.api_key,
            placeid=place_id,
            fields=constants.PLACE_DETAILS_FIELDS
        )
        url = "{}/{}".format(constants.GOOGLE_PLACE_DETAILS_URL, self.output)
        return self._get(url=url, params=params)["result"]

    def places(self, *, place_ids: List[str]) -> List[Dict]:
        return GoogleCloudApi.threaded(
            callback=self.place,
            kwargs_list=[dict(place_id=place_id) for place_id in place_ids]
        )
