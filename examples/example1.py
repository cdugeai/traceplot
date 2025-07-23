from traceplot.Trace import Trace
from traceplot.BackgroundImage import BackgroundImage
from traceplot.types import PointGeo, BoundingBox
import traceplot.map_providers as map_providers
import traceplot.helpers.gmaps as gmaps
from dotenv import load_dotenv
import os
import gpxpy


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


# 1. Get a list of PointGeo (eg. open GPX, or manual input)

gpx_path = "sample.gpx"
points_geo: list[PointGeo] = loadGpxToPointGeo(gpx_path)

points_geo_manual: list[PointGeo] = [
    PointGeo(2.282259089265323, 48.88677456721743, 50),
    PointGeo(2.2746338, 48.8589385, 52),
    PointGeo(2.3850533122051463, 48.82797239213328, 60),
]

# 2. Setup a Trace
t: Trace = Trace(points_geo=points_geo)

# 3. Load background image (eg. with Google Maps Static API, or local png file)

generated_map: BackgroundImage = map_providers.Gmaps(
    {
        "maptype": "roadmap",
        "gmaps_api_key": os.environ.get("GMAPS_API_KEY"),
    }
).downloadEnclosingMap(
    points_geo=points_geo, out_filename="out/background_paris.png", w_px=640, h_px=640
)

local_map: BackgroundImage = BackgroundImage(
    bbox=(1.0, 2.0, 3.0, 4.0), image_path="path/to/image.png"
)


# 4. Add elements to trace  trace, markers and text to image

# 4.1 Add background image
t.addBackgroundImage(background_img=generated_map)
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
t.save("out/premier_jour.png")
# 4.7 Display map
t.show()
# 4.8 Close Trace
t.close()
