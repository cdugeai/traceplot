Point = tuple[float, float]


class PointGeo:
    lng: float
    lat: float

    def __init__(self, lng: float, lat: float) -> None:
        self.lng = lng
        self.lat = lat


## todo fix
Segment = tuple[float, float]
ZoomLevel = int

BoundingBox = tuple[float, float, float, float]
