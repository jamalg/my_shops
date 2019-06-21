from geopy import distance


class Coordinates:
    __slots__ = ["latitude", "longitude"]

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return "{self.latitude},{self.longitude}".format(self=self)

    def __sub__(self, other) -> float:
        """Substracting two Coordinates instances returns their geodesic distance in meters"""
        return distance.distance(
            (self.latitude, self.longitude),
            (other.latitude, other.longitude)
        ).km * 1000
