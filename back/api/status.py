from flask import Blueprint, jsonify

bp = Blueprint("status", __name__, url_prefix="/api/status")


@bp.route("")
def status():
    return jsonify({"status": "healty"})
