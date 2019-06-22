from datetime import datetime, timezone

from back.config import config
from back.models import helper
from back.models.user import User
from back.models.social import DisLike


def test_fresh_dislikes(user_data, dislike_data, db_session):
    user_id = helper.add_user(user_data)["id"]
    dislike_data["user_id"] = user_id
    dislike_id = helper.add_dislike(dislike_data)["id"]

    user = db_session.query(User).get(user_id)
    dislike = db_session.query(DisLike).get(dislike_id)

    assert len(user.fresh_dislikes) == 1
    assert user.fresh_dislikes[0].id == dislike_id

    # Update created_at
    dislike.created_at = datetime.now(tz=timezone.utc) - config.DISLIKE_EXPIRY
    db_session.add(dislike)
    db_session.commit()

    db_session.expunge(user)
    db_session.expunge(dislike)

    user = db_session.query(User).get(user_id)
    assert len(user.fresh_dislikes) == 0


def test_purge_dislikes_helpers(user_data, dislike_data, db_session):
    user_id = helper.add_user(user_data)["id"]
    dislike_data["user_id"] = user_id

    nbr_dislikes = 5
    [helper.add_dislike(dislike_data)["id"] for _ in range(nbr_dislikes)]

    user = db_session.query(User).get(user_id)

    assert db_session.query(DisLike).count() == nbr_dislikes

    user._dislikes[0].created_at = datetime.now(tz=timezone.utc) - config.DISLIKE_EXPIRY
    user._dislikes[1].created_at = datetime.now(tz=timezone.utc) - config.DISLIKE_EXPIRY

    db_session.add(user._dislikes[0])
    db_session.add(user._dislikes[1])
    db_session.commit()

    helper.purge_dislikes()
    assert db_session.query(DisLike).count() == nbr_dislikes - 2
