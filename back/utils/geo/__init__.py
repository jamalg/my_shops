class Coordinate:
    __slots__ = ["latitude", "longitude"]

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return "{self.latitude},{self.longitude}".format(self=self)
