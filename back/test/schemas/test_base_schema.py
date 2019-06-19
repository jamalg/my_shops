from datetime import datetime, timezone

from back.schemas.base import BaseSchema
from back.models.base import Base


class MySchema(BaseSchema):
    __model__ = Base


def test_load_return_model_object():
    data = {
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "updated_at": datetime.now(tz=timezone.utc).isoformat()
    }
    ressource, errors = MySchema().load(data)
    assert isinstance(ressource, Base) is True
    assert isinstance(ressource, dict) is False


def test_partial_load_returns_dict():
    data = {
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "updated_at": datetime.now(tz=timezone.utc).isoformat()
    }
    ressource, errors = MySchema(partial=True).load(data)
    assert isinstance(ressource, Base) is False
    assert isinstance(ressource, dict) is True
