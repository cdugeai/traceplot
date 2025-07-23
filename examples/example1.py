from traceplot.Trace import Trace
from traceplot.types import PointGeo, BoundingBox
from traceplot.map_providers import MapProvider, Gmaps
import traceplot.helpers.gmaps as gmaps
from dotenv import load_dotenv
import os
import gpxpy


load_dotenv()  # take environment variables


def loadGpxToPointGeo(file_path: str) -> [PointGeo]:
    """
    Load a gpx file as a list of PointGeo
    """
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


# 1. Open GPX
gpx_path = "sample.gpx"

points_geo = loadGpxToPointGeo(gpx_path)
points_geo_old: [PointGeo] = [
    PointGeo(2.282259089265323, 48.88677456721743, 50),
    PointGeo(2.2746338, 48.8589385, 52),
    PointGeo(2.3850533122051463, 48.82797239213328, 60),
]

# 2. Generate backgound image (eg. with Google Maps Static API)
FIG_PATH = "out/background_paris.png"
api_key = os.environ.get("GMAPS_API_KEY")

gmaps_provider: MapProvider = Gmaps(
    {
        "maptype": "roadmap",
        "gmaps_api_key": api_key,
    }
)
backgound_map_bbox: BoundingBox = gmaps_provider.downloadEnclosingMap(
    points_geo=points_geo, out_filename=FIG_PATH, w_px=640, h_px=640
)

# 3. Add trace, markers and text to image

t: Trace = Trace(background_bbox=backgound_map_bbox, points_geo=points_geo)

t.addBackgroundImage(background_img_path=FIG_PATH)
t.addMarker(
    points_geo[0],
    img_path="img/marker_start.png",
    label_text="debut",
    marker_scale=0.5,
    label_offset_x=0.05,
)
t.addMarker(
    points_geo[-1],
    img_path="img/marker_finish.png",
    label_text="fin",
    marker_scale=0.5,
    label_offset_x=0.05,
)

t.addElevationGraph(height_pct=0.17, backgroundColor="white", backgroundColorAlpha=0.6)
t.plotPoints()
t.addTitle("Premier jour", center_x=0.5, center_y=0.2, fontsize=30)

t.save("out/premier_jour.png")

t.show()

t.close()
