from traceplot.types import Point, PointGeo, Segment


def getSquareDistance(p1: Point, p2: Point) -> float:
    """
    Square distance between two points
    """
    dx = p1[1] - p2[1]
    dy = p1[0] - p2[0]

    return dx * dx + dy * dy


def getSquareSegmentDistance(p: Segment, p1: Point, p2: Point) -> float:
    """
    Square distance between point and a segment
    """
    x = p1[1]
    y = p1[0]

    dx = p2[1] - x
    dy = p2[0] - y

    if dx != 0 or dy != 0:
        t = ((p[1] - x) * dx + (p[0] - y) * dy) / (dx * dx + dy * dy)

        if t > 1:
            x = p2[1]
            y = p2[0]
        elif t > 0:
            x += dx * t
            y += dy * t

    dx = p[1] - x
    dy = p[0] - y

    return dx * dx + dy * dy


def _simplifyRadialDistance(points, tolerance):
    length = len(points)
    prev_point = points[0]
    new_points = [prev_point]

    for i in range(length):
        point = points[i]

        if getSquareDistance(point, prev_point) > tolerance:
            new_points.append(point)
            prev_point = point

    if prev_point != point:
        new_points.append(point)

    return new_points


def _simplifyDouglasPeucker(points, tolerance):
    length = len(points)
    markers = [0] * length  # Maybe not the most efficent way?

    first = 0
    last = length - 1

    first_stack = []
    last_stack = []

    new_points = []

    markers[first] = 1
    markers[last] = 1

    while last:
        max_sqdist = 0

        for i in range(first, last):
            sqdist = getSquareSegmentDistance(points[i], points[first], points[last])

            if sqdist > max_sqdist:
                index = i
                max_sqdist = sqdist

        if max_sqdist > tolerance:
            markers[index] = 1

            first_stack.append(first)
            last_stack.append(index)

            first_stack.append(index)
            last_stack.append(last)

        # Can pop an empty array in Javascript, but not Python, so check
        # the length of the list first
        if len(first_stack) == 0:
            first = None
        else:
            first = first_stack.pop()

        if len(last_stack) == 0:
            last = None
        else:
            last = last_stack.pop()

    for i in range(length):
        if markers[i]:
            new_points.append(points[i])

    return new_points


def simplify(points, tolerance=0.1, highestQuality=True):
    sqtolerance = tolerance * tolerance

    if not highestQuality:
        points = _simplifyRadialDistance(points, sqtolerance)

    points = _simplifyDouglasPeucker(points, sqtolerance)

    return points


# TODO test this
def pointGeoToPoint(p_geo: PointGeo, minx, miny, maxx, maxy) -> Point:
    return (p_geo.lng - minx) / (maxx - minx), (p_geo.lat - miny) / (maxy - miny)
