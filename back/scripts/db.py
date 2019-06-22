import string
import random
import secrets

from click import Group, option

from back.models import helper

ALPHANUMERIC = string.ascii_letters + string.digits
MIN_PLACE_ID_LEN = 20
MAX_PLACE_ID_LEN = 256

db_cli = Group("db")


def generate_place_id():
    # See for information about Google place_id https://developers.google.com/places/web-service/place-id
    id_len = random.randint(MIN_PLACE_ID_LEN, MAX_PLACE_ID_LEN)
    return "".join(secrets.choice(ALPHANUMERIC) for _ in range(id_len))


@db_cli.command("fill")
@option("--likes", default=5, help="Number of likes")
@option("--dislikes", default=5, help="Number of dislikes")
def fill_db(likes, dislikes):
    user_data = dict(
        first_name="United",
        last_name="Remote",
        email="shops@unitedremote.com",
        password="unitedremote"
    )
    user_id = helper.add_user(user_data)["id"]
    likes = [dict(place_id=generate_place_id(), user_id=user_id) for _ in range(likes)]
    dislikes = [dict(place_id=generate_place_id(), user_id=user_id) for _ in range(dislikes)]
    [helper.add_like(like) for like in likes]
    [helper.add_dislike(dislike) for dislike in dislikes]

# The command could be called once every deploy within CI/CD routines
# Another option could be to configure a database trigger but it has
# a higher performance cost
@db_cli.command("purge-dislikes")
def purge_dislikes():
    helper.purge_dislikes()
