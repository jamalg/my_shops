import io

from flask import Blueprint, send_file
from flask_login import login_required

from back.config import config
from back.extensions.google import google_client

bp = Blueprint("photos", __name__, url_prefix="/api/photos")


@bp.route("/<string:photo_reference>", methods=["GET"])
@login_required
def get_photo(photo_reference):
    image = google_client.photo(photo_reference=photo_reference, max_height=config.GOOGLE_PHOTO_MAX_HEIGHT)
    return send_file(
        io.BytesIO(image.binary),
        mimetype=image.mimetype,
    )
