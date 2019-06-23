from flask import Blueprint, jsonify, request, url_for
from flask_login import current_user, login_required

from back.utils.geo import Coordinates
from back.extensions.google import google_client
from back.config import config
from back.api import utils
from back.schemas.place import PlaceSchema

bp = Blueprint("places", __name__, url_prefix="/api/places")


@bp.route("/nearby", methods=["GET"])
@login_required
def get_nearby_shops():
    try:
        latitude, longitude = float(request.args.get("latitude")), float(request.args.get("longitude"))
    except ValueError:
        return jsonify({"message": "Expecting both 'latitude' and 'longitude' float query parameters"})

    user_location = Coordinates(latitude=latitude, longitude=longitude)
    nearby_shops = google_client.nearby(
        location=Coordinates.discrete_from_location(user_location),
        radius=config.DEFAULT_NEARBY_RADIUS,
        type=config.DEFAULT_NEARBY_TYPE
    )
    filtered_nearby_shops = utils.filter_nearby_places(
        places=nearby_shops,
        filter_out=[social.place_id for social in current_user.likes + current_user.fresh_dislikes]
    )
    context = dict(
        location=user_location,
        photo_api_url=url_for("photos.get_photo", photo_reference="", _external=True)
    )
    return jsonify(PlaceSchema(many=True, context=context).dump(filtered_nearby_shops).data)


@bp.route("/likes", methods=["GET"])
@login_required
def get_liked_places():
    latitude, longitude = request.args.get("latitude"), request.args.get("longitude")
    user_location = None
    if latitude and longitude:
        try:
            latitude, longitude = float(latitude), float(longitude)
            user_location = Coordinates(latitude=latitude, longitude=longitude)
        except ValueError:
            return jsonify({"message": "'latitude' or 'longitude' invalid floats"})

    liked_places = google_client.places(place_ids=[like.place_id for like in current_user.likes])
    context = dict(
        photo_api_url=url_for("photos.get_photo", photo_reference="", _external=True)
    )
    if user_location:
        context["user_location"] = user_location
    return jsonify(PlaceSchema(many=True, context=context).dump(liked_places).data)
