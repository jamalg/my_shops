from typing import List, Dict


def filter_nearby_places(places: List[Dict], filter_out: List[str]) -> List[Dict]:
    places_by_place_id = {place["place_id"]: place for place in places}
    for place_id in filter_out:
        places_by_place_id.pop(place_id, None)
    return places_by_place_id.values()
