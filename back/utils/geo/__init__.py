from geopy import distance

EPSILON = 0.008


class Coordinates:
    __slots__ = ["latitude", "longitude"]

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return "{self.latitude},{self.longitude}".format(self=self)

    def __repr__(self) -> str:
        return "{}({})".format(self.__class__.__name__, self.__str__())

    def __sub__(self, other) -> float:
        """Substracting two Coordinates instances returns their geodesic distance in meters"""
        return distance.distance(
            (self.latitude, self.longitude),
            (other.latitude, other.longitude)
        ).km * 1000

    def __eq__(self, other) -> bool:
        return self.latitude == other.latitude and self.longitude == other.longitude

    @classmethod
    def discrete_location(cls, latitude: float, longitude: float) -> object:
        """
        The main idea here is that we have A=Coordinates(latA, lngA) and B=Coordinates(latB, lngB)
        such as A ~~ B then making two location calls to GooglePlaceAPI is useless and we can assume
        that nearby(A) ~~ nearby(B).

        We say that given circle C of radius R and a regular mesh of it's surface area such as each square S
        has an area such as Area(S) = 10% Area(C) then points within S should be considered the same
        from the point of view of nearby search API.

        The problem boils down to finding the step Epsilone such as:
            - A    = Coordinates(latA           , lngA           )
            - AEps = Coordinates(latA + Epsilone, lngA + Epsilone)
            Area(Square(A-AEps)) = 0.1 * PI * R ** 2

            -->
            Area(Square(A-AEps)) = (Distance(A, AEps) ** 2) / 2 = 0.1 * PI * R ** 2
            With very rough numerical estimate for R=1500 Eps ~ 0.008
        """
        discrte_latitude = latitude - (latitude % EPSILON)
        discrte_longitude = longitude - (longitude % EPSILON)
        return cls(latitude=discrte_latitude, longitude=discrte_longitude)

    @classmethod
    def discrete_from_location(cls, location) -> object:
        return cls.discrete_location(
            latitude=location.latitude, longitude=location.longitude
        )
