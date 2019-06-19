from back.schemas.social import LikeSchema, DisLikeSchema


def test_like_schema(like_data):
    like, errors = LikeSchema().load(like_data)
    assert errors == {}
    assert like.place_id == like_data["place_id"]
    assert like.user_id == like_data["user_id"]


def test_like_required_values():
    _, errors = LikeSchema().load({})
    assert len(errors["user_id"]) == 1 and "required" in errors["user_id"][0]
    assert len(errors["place_id"]) == 1 and "required" in errors["place_id"][0]


def test_dislike_schema(dislike_data):
    dislike, errors = DisLikeSchema().load(dislike_data)
    assert errors == {}
    assert dislike.place_id == dislike_data["place_id"]
    assert dislike.user_id == dislike_data["user_id"]


def test_dislike_required_values():
    _, errors = DisLikeSchema().load({})
    assert len(errors["user_id"]) == 1 and "required" in errors["user_id"][0]
    assert len(errors["place_id"]) == 1 and "required" in errors["place_id"][0]
