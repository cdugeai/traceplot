from traceplot.types import BoundingBox, PointGeo, Point
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from traceplot.helpers.geo import pointGeoToPoint
from matplotlib.patches import Rectangle
from numpy import linspace


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
    pass


class Trace:
    background_bbox: BoundingBox
    fig: plt.Figure
    ax: plt.Axes
    points_px: [Point]
    elevation: [float]

    def __init__(
        self,
        background_img_bbox: BoundingBox,
        points_geo: [PointGeo],
    ):
        FIGSIZE = (10, 10)

        self.background_bbox = background_img_bbox
        self.points_px: [Point] = self._convertPointGeotoPx(points_geo)
        self.elevation: [float] = self._extractElevation(points_geo)

        self.fig, self.ax = plt.subplots(figsize=FIGSIZE)
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1, wspace=0)

        print("fig", self.fig)

        pass

    def _convertPointGeotoPx(self, points_geo):
        [minx, miny, maxx, maxy] = self.background_bbox
        return [pointGeoToPoint(p, minx, miny, maxx, maxy) for p in points_geo]

    def _extractElevation(self, points_geo):
        return [p.ele for p in points_geo]

    def addMarker(
        self,
        point: PointGeo,
        img_path: str,
        label_text: str,
        marker_scale: float = 1.0,
        label_fontsize=20,
        label_offset_x: float = 0,
        label_offset_y: float = 0,
    ) -> None:
        minx, miny, maxx, maxy = self.background_bbox
        point_xy = pointGeoToPoint(point, minx, miny, maxx, maxy)
        imagebox_marker = OffsetImage(Image.open(img_path), zoom=marker_scale)
        # add marker
        self.ax.add_artist(
            AnnotationBbox(
                imagebox_marker,
                point_xy,
                xycoords="data",
                frameon=False,
                box_alignment=(0.5, 0),
            )
        )
        # add label
        self.ax.text(
            point_xy[0] + label_offset_x,
            point_xy[1] + label_offset_y,
            label_text,
            fontsize=label_fontsize,
            bbox=dict(
                boxstyle="round",
                ec=(1.0, 0.5, 0.5),
                fc=(1.0, 0.8, 0.8),
            ),
        )
        pass

    def addBackgroundImage(self, background_img_path: str):
        # Load backgroud image
        self.ax.imshow(Image.open(background_img_path), extent=(0, 1, 0, 1))

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    def addElevationGraph(
        self,
        height_pct: float,
        backgroundColor: str,
        backgroundColorAlpha: float,
    ) -> None:
        PICTURE_HEIGHT = 1
        height_px = height_pct * PICTURE_HEIGHT
        # Add rectangle
        self.ax.add_patch(
            Rectangle(
                xy=(0, 0),
                width=1,
                height=height_px,
                facecolor=backgroundColor,
                alpha=backgroundColorAlpha,
            )
        )

        Y_BOTTOM_SCALE = 0.02
        Y_UPPER_SCALE = height_px - Y_BOTTOM_SCALE  # 0.08
        X_LEFT_SCALE = 0.1
        X_RIGHT_SCALE = 0.9

        min_elev, max_elev = min(self.elevation), max(self.elevation)
        elevation_norm_x = linspace(
            X_LEFT_SCALE, X_RIGHT_SCALE, len(self.elevation)
        ).tolist()
        elevation_norm_y = [
            (elev - min_elev) / (max_elev - min_elev) * (Y_UPPER_SCALE - Y_BOTTOM_SCALE)
            + Y_BOTTOM_SCALE
            for elev in self.elevation
        ]

        self.ax.plot(elevation_norm_x, elevation_norm_y, "b-")

        elevation_legend_x = [X_LEFT_SCALE, X_LEFT_SCALE]
        elevation_legend_y = [Y_BOTTOM_SCALE, Y_UPPER_SCALE]
        self.ax.plot(
            elevation_legend_x, elevation_legend_y, color="grey", linestyle="-"
        )

        ## Ticks

        TICK_SPACE_METERS = 200

        k = -TICK_SPACE_METERS
        list_scale_ticks = [min_elev]
        while k < min_elev:
            k += TICK_SPACE_METERS
        while k <= max_elev:
            list_scale_ticks.append(k)
            k += TICK_SPACE_METERS
        list_scale_ticks.append(max_elev)

        X_SCALE_TICKS = 0.005
        list_y_ticks = list(
            map(
                lambda x: Y_BOTTOM_SCALE
                + (x - min_elev)
                / (max_elev - min_elev)
                * (Y_UPPER_SCALE - Y_BOTTOM_SCALE),
                list_scale_ticks,
            )
        )
        for y_tick in list_y_ticks:
            x = [X_LEFT_SCALE - X_SCALE_TICKS, X_LEFT_SCALE]
            y = [y_tick, y_tick]
            self.ax.plot(x, y, color="grey", linestyle="-")

        # Min max scale
        X_SCALE_LEGEND_OFFSET = 0.01
        FONTSIZE_SCALE = 10
        self.ax.text(
            X_LEFT_SCALE - X_SCALE_LEGEND_OFFSET,
            Y_UPPER_SCALE,
            f"{round(max_elev)}m",
            verticalalignment="center",
            horizontalalignment="right",
            transform=self.ax.transAxes,
            fontsize=FONTSIZE_SCALE,
            color="grey",
        )
        self.ax.text(
            X_LEFT_SCALE - X_SCALE_LEGEND_OFFSET,
            Y_BOTTOM_SCALE,
            f"{round(min_elev)}m",
            verticalalignment="center",
            horizontalalignment="right",
            transform=self.ax.transAxes,
            fontsize=FONTSIZE_SCALE,
            color="grey",
        )

    def build(self):
        self.addElevationGraph("red", 0.2)
        # Add start marker
        self.addMarker()
        # Add finish merker
        self.addMarker()

        pass

    def addTitle(self, title: str, center_x: float, center_y: float, fontsize: int):
        self.ax.text(
            center_x,
            center_y,
            title,
            verticalalignment="center",
            horizontalalignment="center",
            transform=self.ax.transAxes,
            fontsize=fontsize,
        )

    def plotPoints(self):
        self.ax.plot([p[0] for p in self.points_px], [p[1] for p in self.points_px])

    def save(self, outfile_img_path: str):
        plt.savefig(
            outfile_img_path,
            dpi=600,
            pad_inches=0.01,
        )

    def close(self):
        plt.close()

    def show(self):
        plt.show()
