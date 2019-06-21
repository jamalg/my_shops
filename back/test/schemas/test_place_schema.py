from back.utils.geo import Coordinates
from back.schemas.place import PlaceSchema


def test_place_schema_with_all_values(place_data):
    me = Coordinates(33.593008, -7.596878)
    place_location = Coordinates(
        place_data["geometry"]["location"]["lat"],
        place_data["geometry"]["location"]["lng"]
    )
    context = {
        "photo_api_url": "http://test/api/photo/",
        "location": me
    }
    dumped, errors = PlaceSchema(context=context).dump(place_data)
    assert errors == {}
    assert dumped["id"] == place_data["place_id"]
    assert dumped["name"] == place_data["name"]
    assert dumped["vicinity"] == place_data["vicinity"]
    assert dumped["address"] == place_data["formatted_address"]
    assert dumped["latitude"] == place_data["geometry"]["location"]["lat"]
    assert dumped["longitude"] == place_data["geometry"]["location"]["lng"]
    assert dumped["photo_attributions"] == place_data["photos"][0]["html_attributions"][0]
    assert dumped["photo_url"] == "{}{}".format(context["photo_api_url"], place_data["photos"][0]["photo_reference"])
    assert dumped["distance_to_location"] - (me - place_location) < 1


def test_place_schema_without_context(place_data):
    dumped, errors = PlaceSchema().dump(place_data)
    assert errors == {}
    assert dumped["id"] == place_data["place_id"]
    assert dumped["name"] == place_data["name"]
    assert dumped["vicinity"] == place_data["vicinity"]
    assert dumped["address"] == place_data["formatted_address"]
    assert dumped["latitude"] == place_data["geometry"]["location"]["lat"]
    assert dumped["longitude"] == place_data["geometry"]["location"]["lng"]
    assert dumped["photo_attributions"] == place_data["photos"][0]["html_attributions"][0]
    assert dumped["photo_url"] == ""
    assert dumped["distance_to_location"] == 0.0


def test_place_schema_without_photos(place_data):
    me = Coordinates(33.593008, -7.596878)
    place_location = Coordinates(
        place_data["geometry"]["location"]["lat"],
        place_data["geometry"]["location"]["lng"]
    )
    context = {
        "photo_api_url": "http://test/api/photo/",
        "location": me
    }
    place_data.pop("photos")
    dumped, errors = PlaceSchema(context=context).dump(place_data)
    assert errors == {}
    assert dumped["id"] == place_data["place_id"]
    assert dumped["name"] == place_data["name"]
    assert dumped["vicinity"] == place_data["vicinity"]
    assert dumped["address"] == place_data["formatted_address"]
    assert dumped["latitude"] == place_data["geometry"]["location"]["lat"]
    assert dumped["longitude"] == place_data["geometry"]["location"]["lng"]
    assert dumped["photo_attributions"] == ""
    assert dumped["photo_url"] == ""
    assert dumped["distance_to_location"] - (me - place_location) < 1
