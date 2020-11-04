from ..main import Triangulation


def xtest_find_neighbour_sharing_edge():

    t = Triangulation(7, testing=True)

    t.T.list = {
        0: {'id': 0, 'vtx_ids': [6, -1, -2], 'parent_ids': [], 'child_ids': [1, 2, 3]},
        1: {'id': 1, 'vtx_ids': [0, 6, -1], 'parent_ids': [0], 'child_ids': [4, 5, 6]},
        2: {'id': 2, 'vtx_ids': [0, 6, -2], 'parent_ids': [0], 'child_ids': [10, 11]},
        3: {'id': 3, 'vtx_ids': [0, -1, -2], 'parent_ids': [0], 'child_ids': []},
        4: {'id': 4, 'vtx_ids': [1, 0, 6], 'parent_ids': [1], 'child_ids': [12, 13]},
        5: {'id': 5, 'vtx_ids': [1, 0, -1], 'parent_ids': [1], 'child_ids': []},
        6: {'id': 6, 'vtx_ids': [1, 6, -1], 'parent_ids': [1], 'child_ids': [7, 8, 9]},
        7: {'id': 7, 'vtx_ids': [2, 1, 6], 'parent_ids': [6], 'child_ids': [14, 15]},
        8: {'id': 8, 'vtx_ids': [2, 1, -1], 'parent_ids': [6], 'child_ids': []},
        9: {'id': 9, 'vtx_ids': [2, 6, -1], 'parent_ids': [6], 'child_ids': [16, 17, 18]},
        10: {'id': 10, 'vtx_ids': [3, 0, -2], 'parent_ids': [2], 'child_ids': []},
        11: {'id': 11, 'vtx_ids': [3, 6, -2], 'parent_ids': [2], 'child_ids': []},
        12: {'id': 12, 'vtx_ids': [3, 0, 1], 'parent_ids': [4], 'child_ids': []},
        13: {'id': 13, 'vtx_ids': [3, 6, 1], 'parent_ids': [4], 'child_ids': [14, 15]},
        14: {'id': 14, 'vtx_ids': [3, 2, 6], 'parent_ids': [13, 7], 'child_ids': [19, 20]},
        15: {'id': 15, 'vtx_ids': [3, 2, 1], 'parent_ids': [13, 7], 'child_ids': []},
        16: {'id': 16, 'vtx_ids': [4, 2, 6], 'parent_ids': [9], 'child_ids': [19, 20]},
        17: {'id': 17, 'vtx_ids': [4, 2, -1], 'parent_ids': [9], 'child_ids': []},
        18: {'id': 18, 'vtx_ids': [4, 6, -1], 'parent_ids': [9], 'child_ids': []},
        19: {'id': 19, 'vtx_ids': [4, 3, 2], 'parent_ids': [16, 14], 'child_ids': []},
        20: {'id': 20, 'vtx_ids': [4, 3, 6], 'parent_ids': [16, 14], 'child_ids': []}
    }

    nb_ids = t.T.find_neighbour_sharing_edge([2, 3])

    assert nb_ids == {15, 19}

    t.T.list = {
        0: {'id': 0, 'vtx_ids': [6, -1, -2], 'parent_ids': [], 'child_ids': [1, 2, 3]},
        1: {'id': 1, 'vtx_ids': [0, 6, -1], 'parent_ids': [0], 'child_ids': [4, 5, 6]},
        2: {'id': 2, 'vtx_ids': [0, 6, -2], 'parent_ids': [0], 'child_ids': [10, 11]},
        3: {'id': 3, 'vtx_ids': [0, -1, -2], 'parent_ids': [0], 'child_ids': []},
        4: {'id': 4, 'vtx_ids': [1, 0, 6], 'parent_ids': [1], 'child_ids': [12, 13]},
        5: {'id': 5, 'vtx_ids': [1, 0, -1], 'parent_ids': [1], 'child_ids': []},
        6: {'id': 6, 'vtx_ids': [1, 6, -1], 'parent_ids': [1], 'child_ids': [7, 8, 9]},
        7: {'id': 7, 'vtx_ids': [2, 1, 6], 'parent_ids': [6], 'child_ids': [14, 15]},
        8: {'id': 8, 'vtx_ids': [2, 1, -1], 'parent_ids': [6], 'child_ids': []},
        9: {'id': 9, 'vtx_ids': [2, 6, -1], 'parent_ids': [6], 'child_ids': [16, 17, 18]},
        10: {'id': 10, 'vtx_ids': [3, 0, -2], 'parent_ids': [2], 'child_ids': []},
        11: {'id': 11, 'vtx_ids': [3, 6, -2], 'parent_ids': [2], 'child_ids': []},
        12: {'id': 12, 'vtx_ids': [3, 0, 1], 'parent_ids': [4], 'child_ids': []},
        13: {'id': 13, 'vtx_ids': [3, 6, 1], 'parent_ids': [4], 'child_ids': [14, 15]},
        14: {'id': 14, 'vtx_ids': [3, 2, 6], 'parent_ids': [13, 7], 'child_ids': [19, 20]},
        15: {'id': 15, 'vtx_ids': [3, 2, 1], 'parent_ids': [13, 7], 'child_ids': [21, 22]},
        16: {'id': 16, 'vtx_ids': [4, 2, 6], 'parent_ids': [9], 'child_ids': [19, 20]},
        17: {'id': 17, 'vtx_ids': [4, 2, -1], 'parent_ids': [9], 'child_ids': []},
        18: {'id': 18, 'vtx_ids': [4, 6, -1], 'parent_ids': [9], 'child_ids': []},
        19: {'id': 19, 'vtx_ids': [4, 3, 2], 'parent_ids': [16, 14], 'child_ids': [21, 22]},
        20: {'id': 20, 'vtx_ids': [4, 3, 6], 'parent_ids': [16, 14], 'child_ids': []},
        21: {'id': 21, 'vtx_ids': [4, 1, 2], 'parent_ids': [19, 15], 'child_ids': []},
        22: {'id': 22, 'vtx_ids': [4, 1, 3], 'parent_ids': [19, 15], 'child_ids': []}
    }

    nb_ids = t.T.find_neighbour_sharing_edge([2, 1])

    assert nb_ids == {8, 21}
