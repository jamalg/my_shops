from datetime import timezone

from sqlalchemy.types import TypeDecorator, DateTime


class UTCDateTime(TypeDecorator):
    """Custom datetime types that:
    - Only accepts *aware* :class:`~datetime.datetime` objects
    - Always writes *aware* datetimes as UTC to db
    - Raise :exc:`ValueError` if *naive* datetime is given
    """

    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if value.tzinfo is None:
                raise ValueError("Only aware datetime are allowed")
        return value.astimezone(timezone.utc)

    def process_result_value(self, value, dialect):
        return value
