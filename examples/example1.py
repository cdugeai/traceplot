from traceplot.helpers import greet
from traceplot.helpers.gmaps import generate_map_png, degree_to_meter_at_lat
from traceplot.Trace import Trace
from traceplot.types import PointGeo
from dotenv import load_dotenv
from traceplot.helpers.gpx import loadGpxToPointGeo
from traceplot.helpers.geo import getBoundingBox, getCenterOfBoundingBox, getDistanceDeg
from traceplot.helpers.gmaps import downloadEnclosingMap

import os

load_dotenv()  # take environment variables

# 1. Open GPX
gpx_path = "sample.gpx"

points_geo = loadGpxToPointGeo(gpx_path)
points_geo_old: [PointGeo] = [
    PointGeo(2.282259089265323, 48.88677456721743, 50),
    PointGeo(2.2746338, 48.8589385, 52),
    PointGeo(2.3850533122051463, 48.82797239213328, 60),
]


# 2. Generate backgound image
FIG_PATH = "out/background_paris.png"
api_key = os.environ.get("GMAPS_API_KEY")

bbox_png = downloadEnclosingMap(
    points_geo=points_geo,
    out_filename=FIG_PATH,
    gmaps_api_key=api_key,
    maptype="roadmap",
    w_px=640,
    h_px=640,
)


# 3. Add trace, markers and text to image

t: Trace = Trace(background_img_bbox=bbox_png, points_geo=points_geo)

t.addBackgroundImage(FIG_PATH)
t.addMarker(points_geo[0], "img/marker_start.png", "debut", 0.5, label_offset_x=0.05)
t.addMarker(points_geo[-1], "img/marker_finish.png", "fin", 0.5, label_offset_x=0.05)

t.addElevationGraph(height_pct=0.17, backgroundColor="white", backgroundColorAlpha=0.6)
t.plotPoints()
t.addTitle("Premier jour", 0.5, 0.2, 30)

t.save("out/premier_jour.png")

t.show()

t.close()
