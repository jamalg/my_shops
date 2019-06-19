import logging

from flask import Blueprint, request, jsonify
from back.utils.sqlalchemy.helpers import session_manager

from back.models import helper, db
from back.models.user import User
from back.schemas.user import UserSchema

bp = Blueprint("user", __name__, url_prefix="/api/users")
logger = logging.getLogger(__name__)


@bp.route("", methods=["POST"])
def post_user():
    user_data = request.json
    if user_data:
        validation_errors = UserSchema().validate(user_data)
        if validation_errors:
            return jsonify(validation_errors), 400

        # Check that email is unique
        with session_manager(db.session) as db_session:
            if db_session.query(User).filter(User.email == user_data["email"]).first():
                return jsonify({"email": "This email is already used"}), 400

        created_user = helper.add_user(user_data)
        return jsonify(created_user), 201
    return jsonify({"message": "Empty json payload"}), 400
