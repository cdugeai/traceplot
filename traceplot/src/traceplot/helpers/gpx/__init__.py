import gpxpy
import gpxpy.gpx
from traceplot.types import PointGeo


def loadGpxToPointGeo(file_path: str) -> [PointGeo]:
    points = list()
    gpx_file = open(file_path, "r")
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(
                    PointGeo(
                        lng=point.longitude,
                        lat=point.latitude,
                        elevation=point.elevation,
                    )
                )

    return points
