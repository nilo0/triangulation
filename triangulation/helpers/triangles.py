from . import points as points_helper


def new(id, vertices_ids, parent_ids=[], child_ids=[]):
    return {
        'id': id,
        'vertices_ids': vertices_ids,
        'parent_ids': parent_ids,
        'child_ids': child_ids,
    }
