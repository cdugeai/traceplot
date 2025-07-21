from traceplot.helpers import greet
from traceplot.helpers.gmaps import generate_map_png
from traceplot import figure_map
from dotenv import load_dotenv

import os

load_dotenv()  # take environment variables


api_key = os.environ.get('GMAPS_API_KEY')


FIG_PATH = "out/background_paris.png"

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
