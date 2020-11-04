import numpy as np
from random import random, seed

POINT_DTYPE = [
    ('id', np.int),
    ('lat', np.float64),
    ('lon', np.float64),
    ('elev', np.float64),
]


def new(lat, lon, id=0, elev=0):
    return {
        'id': id,
        'lat': lat,
        'lon': lon,
        'elev': elev,
    }


def _on_a_circle(points, lon, lat):
    if len(points) < 3:
        return False

    for i, a in enumerate(points):
        for j, b in enumerate(points[i+1:]):
            for c in points[i+j+1+1:]:
                d = {'lat': lat, 'lon': lon}
                if det_circle(a, b, c, d) == 0:
                    return True

    return False


def generate_lex_order(N, elev_func, bl, tr, testing=False):
    if testing:
        return generate_test_points()

    points = np.zeros(N, dtype=POINT_DTYPE)

    seed(123456789)

    for i, point in enumerate(points):
        while(True):
            lat = bl['lat'] + random() * (tr['lat'] - bl['lat'])
            lon = bl['lon'] + random() * (tr['lon'] - bl['lon'])
            if not _on_a_circle(points[:i], lat, lon):
                elev = elev_func(lon, lat)
                point['lat'] = lat
                point['lon'] = lon
                point['elev'] = elev
                break

        if i % len(point) / 10 == 0:
            print('Found ' + str(i) + ' points...')

    sort_order = np.argsort(points, order=('lat', 'lon'))
    np.take(points, sort_order, out=points)

    for i, point in enumerate(points):
        point['id'] = i

    return points


def generate_test_points():
    vtx = ((1,0),(9,0),(7,3),(13,2),(7,1),(10,8),(14,8),(12,13),(14,14),(4,15))

    points = np.zeros(len(vtx), dtype=POINT_DTYPE)

    for v, point in zip(vtx, points):
        point['lon'] = v[0]
        point['lat'] = v[1]
        point['elev'] = 0

    sort_order = np.argsort(points, order=('lat', 'lon'))
    np.take(points, sort_order, out=points)

    for i, point in enumerate(points):
        point['id'] = i

    return points


def det(a, b, c):
    """
    if det < 0, counter-clockwise order
    if det > 0, clockwise order
    """
    array = np.array([
        [a['lon'], a['lat'], 1],
        [b['lon'], b['lat'], 1],
        [c['lon'], c['lat'], 1]
    ])

    return np.linalg.det(array)


def find_left_and_right(a, b):
    return (a, b) if a['id'] < b['id'] else (b, a)


def det_circle(a, b, c, d):
    """
    d : the new node we added to triangulation
    if det = 0, the points lie on a common circle
    if det > 0, d lies inside the common circle of a, b, c
    if det < 0, d lies outside the common circle of a, b, c
    """
    if det(a, b, c) > 0:
        array = np.array([
            [a['lon'], a['lat'], a['lon']**2 + a['lat']**2, 1],
            [b['lon'], b['lat'], b['lon']**2 + b['lat']**2, 1],
            [c['lon'], c['lat'], c['lon']**2 + c['lat']**2, 1],
            [d['lon'], d['lat'], d['lon']**2 + d['lat']**2, 1]
        ])
    else:
        array = np.array([
            [a['lon'], a['lat'], a['lon']**2 + a['lat']**2, 1],
            [c['lon'], c['lat'], c['lon']**2 + c['lat']**2, 1],
            [b['lon'], b['lat'], b['lon']**2 + b['lat']**2, 1],
            [d['lon'], d['lat'], d['lon']**2 + d['lat']**2, 1]
        ])

    return np.linalg.det(array)
