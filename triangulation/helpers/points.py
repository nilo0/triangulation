import numpy as np

POINT_DTYPE = [
    ('id', np.int),
    ('lat', np.float64),
    ('lon', np.float64),
    ('elev', np.float64),
]


def generate_lex_order(N, elev_func, testing=False):
    if testing:
        return generate_test_points()


def generate_test_points():
    vtx = ((0, 0), (1, 0), (2, 0), (0, 2), (2, 2), (-1, 3), (0, 4))

    points = np.zeros(len(vtx), dtype=POINT_DTYPE)

    for v, point in zip(vtx, points):
        point['lat'] = v[0]
        point['lon'] = v[1]
        point['elev'] = 0

    sort_order = np.argsort(points, order=('lat', 'lon'))
    np.take(points, sort_order, out=points)

    for i, point in enumerate(points):
        point['id'] = i

    return points


def det(a, b, c):
    array = np.array([
        [a['lon'], a['lat'], 1],
        [b['lon'], b['lat'], 1],
        [c['lon'], c['lat'], 1]
    ])

    return np.linalg.det(array)


def find_left_and_right(a, b):
    return a, b if a['id'] < b['id'] else b, a
