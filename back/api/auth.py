import logging

from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user, LoginManager

from back.models import db
from back.models.user import User

logger = logging.getLogger(__name__)
login_manager = LoginManager()
bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Empty json"}), 400
    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        return jsonify({"message": "Badly formatted json"}), 400
    user = db.session.query(User).filter(User.email == email).first()
    if user:
        if user.check_password(password):
            login_user(user)
            logger.info(
                "User {} logged in".format(user.email),
                extra={"user_id": user.id}
            )
            return jsonify({"message": "Successful logging"}), 200
    return jsonify({"message": "Bad Credentials"}), 403


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successful logout"})
