from . import points as points_helper


def new(id, vtx_ids, parent_ids, child_ids):
    return {
        'id': id,
        'vtx_ids': vtx_ids,  # vertices ids
        'parent_ids': parent_ids,
        'child_ids': child_ids,
    }


def is_inside(T, point, points):
    vtx_ids = T['vtx_ids']

    # Handle P_1 and P_2
    if point['id'] == -1 or point['id'] == -2:
        if point['id'] in T['vtx_ids']:
            return True
        else:
            return False

    if -1 in vtx_ids and -2 not in vtx_ids:
        id1, id2 = list(set(vtx_ids) - {-1})

        left, right = points_helper.find_left_and_right(
            points[id1], points[id2])

        if point['id'] > left['id'] and point['id'] < right['id'] \
                and points_helper.det(left, right, point) <= 0:
            return True
        else:
            return False

    elif -2 in vtx_ids and -1 not in vtx_ids:
        id1, id2 = list(set(vtx_ids) - {-2})

        left, right = points_helper.find_left_and_right(
            points[id1], points[id2])

        if point['id'] > left['id'] and point['id'] < right['id'] \
                and points_helper.det(left, right, point) >= 0:
            return True
        else:
            return False

    elif -1 in vtx_ids and -2 in vtx_ids:
        id1 = list(set(vtx_ids) - {-1, -2})

        if point['id'] < id1:
            return True
        else:
            return False
    else:
        a = points[T['vtx_ids'][0]]
        b = points[T['vtx_ids'][1]]
        c = points[T['vtx_ids'][2]]

        t0 = points_helper.det(a, b, c)
        t1 = points_helper.det(a, b, point)
        t2 = points_helper.det(a, point, c)
        t3 = points_helper.det(point, b, c)

        if abs(abs(t0) - (abs(t1) + abs(t2) + abs(t3))) < 1e-8:
            return True
        else:
            return False


def common_vertices(T1, T2):
    common = []

    for v in T1['vtx_ids']:
        if v in T2['vtx_ids']:
            common.append(v)

    return common
