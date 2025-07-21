from math import cos, radians, log2, sqrt
import requests
from pyproj import Geod
from traceplot.types import ZoomLevel, BoundingBox


def one_latitude_degree(lat: float) -> float:
    """
    Returns distance in meters
    """
    geod = Geod(ellps="WGS84")
    lon = 0
    lat1 = lat - 0.5
    lat2 = lat + 0.5
    _, _, distance_m = geod.inv(lon, lat1, lon, lat2)
    return distance_m


def get_zoom_level_from_radius(
    latitude: float, radius_meters: float, width_px: int
) -> ZoomLevel:
    meters_per_pixel_at_zoom_0 = 156543.03392
    target_meters_per_pixel = (2 * radius_meters * sqrt(2)) / width_px
    adjusted_mpp = target_meters_per_pixel / cos(radians(latitude))
    zoom_level = log2(meters_per_pixel_at_zoom_0 / adjusted_mpp)
    print(int(round(zoom_level)))
    return int(round(zoom_level))


def get_google_maps_bbox(
    center_lat: float, center_lon: float, zoom: ZoomLevel, width_px: int, height_px: int
) -> BoundingBox:
    scale = 156543.03392 * cos(radians(center_lat)) / (2**zoom)

    # Image dimensions
    image_width_m = width_px * scale
    image_height_m = height_px * scale

    # Conversion from meters in degrees
    lat_deg_per_m = 1 / one_latitude_degree(center_lat)
    lon_deg_per_m = 360 / (40075000 * cos(radians(center_lat)))

    delta_lat = (image_height_m * lat_deg_per_m) / 2
    delta_lon = (image_width_m * lon_deg_per_m) / 2

    minx = center_lon - delta_lon
    maxx = center_lon + delta_lon
    miny = center_lat - delta_lat
    maxy = center_lat + delta_lat

    return minx, miny, maxx, maxy


def create_satellite_figure(
    lat: float,
    lon: float,
    width_px_sat: int,
    height_px_sat: int,
    radius_meters: float,
    figure_path: str,
    gmaps_api_key: str,
) -> BoundingBox:
    zoom = get_zoom_level_from_radius(
        lat, radius_meters, width_px_sat
    )  ###### ADD POTENTIAL OFFSET
    size = str(width_px_sat) + "x" + str(height_px_sat)

    # url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=roadmap&scale=2&key={api_key}"
    url: str = "".join(
        [
            "https://maps.googleapis.com/maps/api/staticmap",
            f"?center={lat},{lon}",
            f"&zoom={zoom}",
            f"&size={size}",
            f"&maptype=roadmap",
            f"&scale=2",
            f"&key={gmaps_api_key}",
        ]
    )

    if requests.get(url).status_code == 200:
        with open(figure_path, "wb") as f:
            f.write(response.content)
            print(
                f"Satellite figure centered on {round(lat, 4)}, {round(lon, 4)} with a {radius_meters}m radius done"
            )

    else:
        print("Erreur :", response.status_code)

    return get_google_maps_bbox(lat, lon, zoom, width_px_sat, height_px_sat)
