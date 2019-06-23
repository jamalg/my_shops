from typing import NamedTuple

BINARY_SEPARATOR = b"|"


class Image(NamedTuple):
    binary: bytes
    filename: str
    mimetype: str

    @staticmethod
    def serialize(image):
        # FIXME Highly experimental
        return BINARY_SEPARATOR.join([image.binary, image.filename.encode(), image.mimetype.encode()])

    @classmethod
    def deserialize(cls, serialized):
        # FIXME Extremely hacky
        *binary, byte_filename, byte_mimetype = serialized.split(BINARY_SEPARATOR)
        binary = BINARY_SEPARATOR.join(binary)
        filename, mimetype = byte_filename.decode(), byte_mimetype.decode()
        return cls(binary=binary, filename=filename, mimetype=mimetype)
