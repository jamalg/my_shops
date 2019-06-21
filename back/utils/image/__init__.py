from typing import NamedTuple


class Image(NamedTuple):
    binary: bytes
    filename: str
    mimetype: str
