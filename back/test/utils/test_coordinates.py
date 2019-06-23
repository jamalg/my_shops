from back.utils.geo import Coordinates, EPSILON


def test_discrete_coordinates():
    base_latitude = 30.0
    base_longitude = 40.0
    base = Coordinates(latitude=base_latitude, longitude=base_longitude)
    assert base == Coordinates.discrete_location(latitude=base_latitude + 0.1 * EPSILON,
        longitude=base_longitude + 0.1 * EPSILON) # noqa
    assert base == Coordinates.discrete_location(latitude=base_latitude + 0.3 * EPSILON,
        longitude=base_longitude + 0.3 * EPSILON) # noqa
    assert base == Coordinates.discrete_location(latitude=base_latitude + 0.5 * EPSILON,
        longitude=base_longitude + 0.5 * EPSILON) # noqa
    assert base == Coordinates.discrete_location(latitude=base_latitude + 0.7 * EPSILON,
        longitude=base_longitude + 0.7 * EPSILON) # noqa
    assert base == Coordinates.discrete_location(latitude=base_latitude + 0.9 * EPSILON,
        longitude=base_longitude + 0.9 * EPSILON) # noqa
    assert base != Coordinates.discrete_location(latitude=base_latitude + EPSILON,
        longitude=base_longitude + EPSILON) # noqa


def test_discrete_from_location():
    base_latitude = 30.0
    base_longitude = 40.0
    baseEps = Coordinates(latitude=base_latitude + 0.1 * EPSILON, longitude=base_longitude + 0.1 * EPSILON)
    assert Coordinates.discrete_from_location(baseEps) == Coordinates.discrete_location(latitude=base_latitude + 0.1 * EPSILON, # noqa
        longitude=base_longitude + 0.1 * EPSILON) # noqa
