GOOGLE_PLACES_BASE_URL = "https://maps.googleapis.com/maps/api/place"
GOOGLE_PLACES_API_SUCCESS_STATUS = "OK"

NEARBY_DIRECTORY = "nearbysearch"
GOOGLE_PLACES_NEARBY_URL = "{}/{}".format(GOOGLE_PLACES_BASE_URL, NEARBY_DIRECTORY)

PLACE_DETAILS_DIRECTORY = "details"
PLACE_DETAILS_FIELDS = (
    "address_component,adr_address,alt_id,formatted_address,geometry,icon,id,name,permanently_closed",
    ",photo,place_id,plus_code,scope,type,url,utc_offset,vicinity"
)[0]
GOOGLE_PLACE_DETAILS_URL = "{}/{}".format(GOOGLE_PLACES_BASE_URL, PLACE_DETAILS_DIRECTORY)

PLACE_PHOTO_DIRECTORY = "photo"
GOOGLE_PLACE_PHOTO_URL = "{}/{}".format(GOOGLE_PLACES_BASE_URL, PLACE_PHOTO_DIRECTORY)