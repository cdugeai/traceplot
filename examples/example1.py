from traceplot.types import PointGeo, BoundingBox
from traceplot.BackgroundImage import BackgroundImage
from traceplot.Trace import Trace
from dotenv import load_dotenv
import traceplot.map_providers as map_providers
import traceplot.helpers.gmaps as gmaps
import gpxpy
import os

load_dotenv()


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


# 1. Get a list of PointGeo
# 1.1 ... from GPX file
gpx_path = "sample.gpx"
points_geo: list[PointGeo] = loadGpxToPointGeo(gpx_path)
# 1.2 ... from manual input
points_geo_manual: list[PointGeo] = [
    PointGeo(2.282259089265323, 48.88677456721743, 50),
    PointGeo(2.2746338, 48.8589385, 52),
    PointGeo(2.3850533122051463, 48.82797239213328, 60),
]

# 2. Setup a Trace
t: Trace = Trace(points_geo=points_geo)

# 3. Load background image
# 3.1 ... Download map using a map provider (eg. with Google Maps Static API)
generated_map: BackgroundImage = map_providers.Gmaps(
    {
        "maptype": "roadmap",
        "gmaps_api_key": os.environ.get("GMAPS_API_KEY"),
    }
).downloadEnclosingMap(
    points_geo=points_geo, out_filename="out/background_paris.png", w_px=640, h_px=640
)
# 3.2 ... or load image from file
local_map: BackgroundImage = BackgroundImage(
    bbox=(2.117, 48.704, 2.557, 48.994), image_path="out/background_paris.png"
)

# 4. Add elements to trace  trace, markers and text to image
# 4.1 Add background image to Trace
ADD_BACKGROUND_IMAGE = True

if ADD_BACKGROUND_IMAGE:
    t.addBackgroundImage(background_img=generated_map)
    # OR t.addBackgroundImage(background_img=local_map)
else:
    # If needed, resize bounding box when no background image added
    t.resizeBbox(margin_bottom=0.5, margin_left=0.1, margin_right=0.1, margin_top=0.0)

# 4.2 Add start/end markers
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
# 4.3 Add elevation graph
t.addElevationGraph(height_pct=0.17, backgroundColor="white", backgroundColorAlpha=0.6)
# 4.4 Plot points
t.plotPoints()
# 4.5 Add title
t.addTitle("Premier jour", center_x=0.5, center_y=0.2, fontsize=30)
# 4.6 Save map to file
t.save("out/day_one.png")
# 4.7 Display map
t.show()
# 4.8 Close Trace
t.close()
