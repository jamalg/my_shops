from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from back.models import helper, db
from back.models.social import Like
from back.schemas.user import UserSchema
from back.schemas.social import LikeSchema, DisLikeSchema
from back.exceptions import _SecurityError


bp = Blueprint("me", __name__, url_prefix="/api/me")


@bp.route("", methods=["GET"])
@login_required
def me():
    return jsonify(UserSchema().dump(current_user).data)


@bp.route("/likes", methods=["POST"])
@login_required
def add_like():
    like_data = request.json
    if like_data:
        if "user_id" in like_data and like_data["user_id"] != current_user.id:
            raise _SecurityError(
                message="Attempt to temper with like user_id",
                data={
                    "user_id": current_user.id,
                    "like_data": like_data
                }
            )
        like_data["user_id"] = current_user.id
        validation_errors = LikeSchema().validate(like_data)
        if validation_errors:
            return jsonify(validation_errors), 400

        created_like = helper.add_like(like_data)
        return jsonify(created_like), 201
    return jsonify({"message": "Empty json payload"}), 400


@bp.route("/dislikes", methods=["POST"])
@login_required
def add_dislike():
    dislike_data = request.json
    if dislike_data:
        if "user_id" in dislike_data and dislike_data["user_id"] != current_user.id:
            raise _SecurityError(
                message="Attempt to temper with dislike user_id",
                data={
                    "user_id": current_user.id,
                    "dislike_data": dislike_data
                }
            )
        dislike_data["user_id"] = current_user.id
        validation_errors = DisLikeSchema().validate(dislike_data)
        if validation_errors:
            return jsonify(validation_errors), 400

        created_dislike = helper.add_dislike(dislike_data)
        return jsonify(created_dislike), 201
    return jsonify({"message": "Empty json payload"}), 400


@bp.route("/likes/<int:like_id>", methods=["DELETE"])
@login_required
def delete_like(like_id):
    user_id = db.session.query(Like.user_id).filter(Like.id == like_id).scalar()
    if user_id:
        if user_id != current_user.id:
            raise _SecurityError(
                message="Attempt to delete like of other user",
                data={
                    "user_id": current_user.id,
                    "like_id": like_id,
                    "targeted_user_id": user_id
                }
            )
        helper.delete_like(like_id)
        return jsonify({"message": "Successful like delete"})
    return jsonify({"message": "Not found"}), 404
