from typing import Dict, Tuple, Optional
import re
import urllib

import requests

from back.utils.geo import Coordinate
from back.extensions.google.exceptions import GoogleApiError
from back.extensions.google import constants


class GoogleCloudApi:
    def __init__(self, api_key: str = None, output: str = "json") -> None:
        self.output = output
        self.api_key = api_key

    def _get(self, url: str, params: Dict) -> Dict:
        url_params = urllib.parse.urlencode(params, safe=",")
        response = requests.get("{}?{}".format(url, url_params))
        if response.ok:
            data = response.json()
            if data["status"] == constants.GOOGLE_PLACES_API_SUCCESS_STATUS:
                return data
            raise GoogleApiError(message=data.get("error_message", data["status"]), data=data)
        raise GoogleApiError.from_http_response(response)

    @staticmethod
    def filename_from_headers(headers: requests.structures.CaseInsensitiveDict) -> str:
        content_disposition = headers.get("content-disposition", None)
        if content_disposition:
            # Need to bulletproof the regexp before "real" go live
            # Don't know exactly why the r is necessary to turn down flake8 error
            match = re.search(r'filename="([\w._\-/]+)"', content_disposition)
            if match:
                return match.group(1)
        image_type = headers["content-type"].split("/")[-1]
        return "image.{}".format(image_type)

    @staticmethod
    def headers_to_photo_metadata(headers: requests.structures.CaseInsensitiveDict) -> Dict:
        mimetype = headers["content-type"]
        filename = GoogleCloudApi.filename_from_headers(headers)
        return dict(
            mimetype=mimetype,
            filename=filename
        )

    def photo(
            self,
            photo_reference: str,
            max_height: Optional[int] = None,
            max_width: Optional[int] = None
            ) -> Tuple[Dict, bytes]:
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
            return GoogleCloudApi.headers_to_photo_metadata(response.headers), response.content
        raise GoogleApiError.from_http_response(response)

    def nearby(self, location: Coordinate, radius: int, type: str) -> Dict:
        params = dict(
            key=self.api_key,
            location=str(location),
            radius=radius,
            type=type
        )
        url = "{}/{}".format(constants.GOOGLE_PLACES_NEARBY_URL, self.output)
        return self._get(url=url, params=params)

    def place(self, place_id: str) -> Dict:
        params = dict(
            key=self.api_key,
            placeid=place_id,
            fields=constants.PLACE_DETAILS_FIELDS
        )
        url = "{}/{}".format(constants.GOOGLE_PLACE_DETAILS_URL, self.output)
        return self._get(url=url, params=params)
