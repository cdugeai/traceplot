from traceplot.helpers import greet
from traceplot.helpers.gmaps import generate_map_png
from traceplot import figure_map
from traceplot.Trace import Trace
from traceplot.types import PointGeo
from dotenv import load_dotenv
from traceplot.helpers.gpx import loadGpxToPointGeo
import os

load_dotenv()  # take environment variables

api_key = os.environ.get("GMAPS_API_KEY")

FIG_PATH = "out/background_paris.png"

## 1. Get background image

# Generate background image
bbox_png = generate_map_png(
    maptype="roadmap",
    lat=48.8589385,
    lon=2.2646338,
    width_px_sat=640,
    height_px_sat=640,
    radius_meters=10000,
    figure_path=FIG_PATH,
    gmaps_api_key=api_key,
)

# Add track to image
figure_map(
    [
        (2.282259089265323, 48.88677456721743, 50),
        (2.2746338, 48.8589385, 55),
        (2.3850533122051463, 48.82797239213328, 60),
    ],
    bbox_png,
    FIG_PATH,
    "out/trace_paris1.png",
    "My first stage",
    "From here",
    "to here",
    "img/marker_start.png",
    "img/marker_finish.png",
)

print("map done")

## 2. Add trace to background

# bbox_png= (2.0449071460262007, 48.71423084169946, 2.484360453973799, 49.00364615830054)
points_geo_old: [PointGeo] = [
    PointGeo(2.282259089265323, 48.88677456721743, 50),
    PointGeo(2.2746338, 48.8589385, 52),
    PointGeo(2.3850533122051463, 48.82797239213328, 60),
]

gpx_path = "sample.gpx"

points_geo = loadGpxToPointGeo(gpx_path)

t: Trace = Trace(background_img_bbox=bbox_png, points_geo=points_geo)

t.addBackgroundImage(FIG_PATH)
t.addMarker(points_geo[0], "img/marker_start.png", "debut", 0.5, label_offset_x=0.05)
t.addMarker(points_geo[-1], "img/marker_finish.png", "fin", 0.5, label_offset_x=0.05)

t.addElevationGraph(height_pct=0.17, backgroundColor="white", backgroundColorAlpha=0.6)
t.plotPoints()
t.addTitle("Premier jour", 0.5, 0.2, 30)

t.show()
