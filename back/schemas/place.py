from typing import Dict

from marshmallow import Schema, fields

from back.utils.geo import Coordinates


class PlaceSchema(Schema):

    place_id = fields.String(dump_to="id")
    name = fields.String()
    photo_url = fields.Method(serialize="build_photo_url")
    photo_attributions = fields.Method(serialize="get_photo_attributions")
    distance_to_location = fields.Method(serialize="compute_distance_to_location")
    latitude = fields.Function(lambda obj: obj["geometry"]["location"]["lat"])
    longitude = fields.Function(lambda obj: obj["geometry"]["location"]["lng"])
    vicinity = fields.String()
    formatted_address = fields.String(dump_to="address")
    like_id = fields.Integer()

    def build_photo_url(self, obj: Dict) -> str:
        if "photos" in obj and "photo_api_url" in self.context:
            return "{}{}".format(self.context["photo_api_url"], obj["photos"][0]["photo_reference"])
        return ""

    def get_photo_attributions(self, obj: Dict) -> str:
        """Extract photo attributions from obj. See examples below :
        {
            ...,
            'photos': [
                {
                    'height': 1836,
                    'html_attributions': ['<a href="https://maps.google.com/maps/contrib/111/photos">Attribution</a>'],
                    'photo_reference': 'CmRaAAAAnQcKO6NRR',
                    'width': 3264
                }
            ],
        }
        """
        return obj.get("photos", [{}])[0].get("html_attributions", [""])[0]

    def compute_distance_to_location(self, obj: Dict) -> float:
        location = self.context.get("location")
        if location:
            place_coordinates = Coordinates(
                latitude=obj["geometry"]["location"]["lat"],
                longitude=obj["geometry"]["location"]["lng"]
            )
            return location - place_coordinates
        return 0.0
