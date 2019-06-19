from back.models import helper, db
from back.models.user import User


def test_user_password(user_data):
    user_id = helper.add_user(user_data)["id"]
    user = db.session.query(User).get(user_id)
    assert user.check_password(user_data["password"]) is True
    assert user.check_password(user_data["password"] + "g") is False
    assert user.check_password(user.password_hash) is False


def test_password_are_random(user_data):
    user_id_1 = helper.add_user(user_data)["id"]
    user_id_2 = helper.add_user({**user_data, "email": "other@mailbox.com"})["id"]

    user_1 = db.session.query(User).get(user_id_1)
    user_2 = db.session.query(User).get(user_id_2)
    assert user_1.password_hash != user_2.password_hash
