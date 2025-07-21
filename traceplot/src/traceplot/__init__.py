import matplotlib.pyplot as plt
from PIL import Image
from shapely.geometry import box, Point, Polygon, MultiPolygon
from pyproj import Geod
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np


def add_trace_to_image(image_path: str, gpx_path: str):
    pass


FONTSIZE_NAME = 30
FONTSIZE_CITIES = 20
FONTSIZE_SCALE = 10
Y_NAME = 0.15
Y_TOP_RECTANGLE_COLOR = Y_NAME + 0.05
Y_UPPER_SCALE = 0.08
Y_BOTTOM_SCALE = 0.02
X_LEFT_SCALE = 0.1
X_RIGHT_SCALE = 0.9
X_SCALE_LEGEND_OFFSET = 0.01
X_SCALE_TICKS = 0.005
TICK_SPACE_METERS = 200
ZOOM_MARKER_START_FINISH = 0.7


## what is it ? TODO
def adjust_text_within_bbox(ax, x, y, text, **kwargs):
    t = ax.text(x, y, text, **kwargs, alpha=0)
    ax.figure.canvas.draw()
    bbox = t.get_window_extent()
    ax_bbox = ax.get_window_extent()
    # Horizontal gap
    dx = 0
    if bbox.x1 > (ax_bbox.x1 - 0.01 * (ax_bbox.x1 - ax_bbox.x0)):
        dx = ax_bbox.x1 - 0.01 * (ax_bbox.x1 - ax_bbox.x0) - bbox.x1
    if bbox.x0 < (ax_bbox.x0 + 0.01 * (ax_bbox.x1 - ax_bbox.x0)):
        dx = ax_bbox.x0 + 0.01 * (ax_bbox.x1 - ax_bbox.x0) - bbox.x0
    # Vertical gap
    dy = 0
    if bbox.y1 > (ax_bbox.y1 - 0.01 * (ax_bbox.y1 - ax_bbox.y0)):
        dy = ax_bbox.y1 - 0.01 * (ax_bbox.y1 - ax_bbox.y0) - bbox.y1
    if bbox.y0 < (ax_bbox.y0 + 0.01 * (ax_bbox.y1 - ax_bbox.y0)):
        dy = ax_bbox.y0 + 0.01 * (ax_bbox.y1 - ax_bbox.y0) - bbox.y0

    inv = ax.transData.inverted()
    x0, y0 = inv.transform((bbox.x0, bbox.y0))
    x1, y1 = inv.transform((bbox.x0 + dx, bbox.y0 + dy))
    dx_data = x1 - x0
    dy_data = y1 - y0
    t = ax.text(x + dx_data, y + dy_data, text, **kwargs)

    return t


def figure_map(
    points,
    bbox_satellite,
    satellite_img_path,
    outfile_img_path,
    name,
    start,
    finish,
    img_start_marker_path,
    img_finish_marker_path,
    offset_start_x=0,
    offset_start_y=0,
    offset_finish_x=0,
    offset_finish_y=0,
):
    [minx, miny, maxx, maxy] = bbox_satellite
    print("bbox_satellite", bbox_satellite)

    elevation = [p[2] for p in points]
    print("elevation", elevation)

    points = [
        ((p[0] - minx) / (maxx - minx), (p[1] - miny) / (maxy - miny)) for p in points
    ]

    img = Image.open(satellite_img_path)
    print(img)

    start_img = Image.open(img_start_marker_path)
    finish_img = Image.open(img_finish_marker_path)
    imagebox_start = OffsetImage(start_img, zoom=ZOOM_MARKER_START_FINISH)
    imagebox_finish = OffsetImage(finish_img, zoom=ZOOM_MARKER_START_FINISH)

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.subplots_adjust(top=1, bottom=0, left=0, right=1, wspace=0)

    # Add satellite figure
    ax.imshow(img, extent=(0, 1, 0, 1))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Pointer print
    ax.add_artist(
        AnnotationBbox(
            imagebox_start,
            points[0],
            xycoords="data",
            frameon=False,
            box_alignment=(0.5, 0),
        )
    )

    # Pointer print
    ax.add_artist(
        AnnotationBbox(
            imagebox_finish,
            points[-1],
            xycoords="data",
            frameon=False,
            box_alignment=(0.5, 0),
        )
    )

    ax.text(
        points[0][0] + offset_start_x,
        points[0][1] + offset_start_y,
        start,
        fontsize=FONTSIZE_CITIES,
        bbox=dict(
            boxstyle="round",
            ec=(1.0, 0.5, 0.5),
            fc=(1.0, 0.8, 0.8),
        ),
    )
    ax.text(
        points[-1][0] + offset_finish_x,
        points[-1][1] + offset_finish_y,
        finish,
        fontsize=FONTSIZE_CITIES,
        bbox=dict(
            boxstyle="round",
            ec=(1.0, 0.5, 0.5),
            fc=(1.0, 0.8, 0.8),
        ),
    )

    for i in range(len(points) - 1):
        x_values = [points[i][0], points[i + 1][0]]
        y_values = [points[i][1], points[i + 1][1]]
        ax.plot(x_values, y_values, "b-")

    print("x_values", x_values)
    print("y_values", y_values)
    ax.add_patch(
        Rectangle(
            xy=(0, 0),
            width=1,
            height=Y_TOP_RECTANGLE_COLOR,
            facecolor="white",
            alpha=0.7,
        )
    )

    # Name
    ax.text(
        0.5,
        Y_NAME,
        name,
        verticalalignment="center",
        horizontalalignment="center",
        transform=ax.transAxes,
        fontsize=FONTSIZE_NAME,
    )

    min_elev, max_elev = min(elevation), max(elevation)
    elevation_norm_x = np.linspace(X_LEFT_SCALE, X_RIGHT_SCALE, len(elevation)).tolist()
    elevation_norm_y = [
        (elev - min_elev) / (max_elev - min_elev) * (Y_UPPER_SCALE - Y_BOTTOM_SCALE)
        + Y_BOTTOM_SCALE
        for elev in elevation
    ]
    ax.plot(elevation_norm_x, elevation_norm_y, "b-")

    elevation_legend_x = [X_LEFT_SCALE, X_LEFT_SCALE]
    elevation_legend_y = [Y_BOTTOM_SCALE, Y_UPPER_SCALE]
    ax.plot(elevation_legend_x, elevation_legend_y, color="grey", linestyle="-")

    print("ticks")

    k = -TICK_SPACE_METERS
    list_scale_ticks = [min_elev]
    while k < min_elev:
        k += TICK_SPACE_METERS
    while k <= max_elev:
        list_scale_ticks.append(k)
        k += TICK_SPACE_METERS
    list_scale_ticks.append(max_elev)

    list_y_ticks = list(
        map(
            lambda x: Y_BOTTOM_SCALE
            + (x - min_elev) / (max_elev - min_elev) * (Y_UPPER_SCALE - Y_BOTTOM_SCALE),
            list_scale_ticks,
        )
    )
    for y_tick in list_y_ticks:
        x = [X_LEFT_SCALE - X_SCALE_TICKS, X_LEFT_SCALE]
        y = [y_tick, y_tick]
        ax.plot(x, y, color="grey", linestyle="-")

    ax.text(
        X_LEFT_SCALE - X_SCALE_LEGEND_OFFSET,
        Y_UPPER_SCALE,
        f"{round(max_elev)}m",
        verticalalignment="center",
        horizontalalignment="right",
        transform=ax.transAxes,
        fontsize=FONTSIZE_SCALE,
        color="grey",
    )
    ax.text(
        X_LEFT_SCALE - X_SCALE_LEGEND_OFFSET,
        Y_BOTTOM_SCALE,
        f"{round(min_elev)}m",
        verticalalignment="center",
        horizontalalignment="right",
        transform=ax.transAxes,
        fontsize=FONTSIZE_SCALE,
        color="grey",
    )

    plt.savefig(
        outfile_img_path,
        dpi=600,
        pad_inches=0.01,
    )

    plt.close()
    print("Map exported")
