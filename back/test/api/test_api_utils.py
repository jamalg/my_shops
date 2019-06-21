from back.api.utils import filter_nearby_places


def test_filtering():
    places_in_ids = "abdeg"
    places_out_ids = "cfh"

    places_in = [dict(place_id=char) for char in places_in_ids]
    places_out = [dict(place_id=char) for char in places_out_ids]
    all_places = places_in + places_out
    filtered = filter_nearby_places(all_places, places_out_ids)
    assert sorted(places_in, key=lambda place: place["place_id"]) == sorted(filtered, key=lambda place: place["place_id"])
