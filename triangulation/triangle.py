import sys

from .helpers import points as points_helper
from .helpers import triangles as triangles_helper


class Triangle:
    def __init__(self, P_1, P_2, points):
        self.P_1 = P_1
        self.P_2 = P_2
        self.P = points

        self.list ={
            0: triangles_helper.new(0, [points[-1]['id'], P_1['id'], P_2['id']], [], [])
        }


    def add(self, vtx_ids, parent_ids, child_ids):
        i = len(self.list)
        self.list[i] = triangles_helper.new(
            len(self.list), vtx_ids, parent_ids, child_ids
        )

        return self.list[i]

    def locate(self, point):
        children_ids = self.list[0]['child_ids']

        found = []

        while children_ids:
            within = []
            for child_id in children_ids:
                child = self.list[child_id]

                if triangles_helper.is_inside(child, point, self.P):
                    within.append(child_id)

            children_ids = []

            for i in within:
                if self.list[i]['child_ids']:
                    children_ids += self.list[i]['child_ids']
                else:
                    found.append(i)

        return found if found else [0]

    def find_neighbour_sharing_edge(self, edge_ids):
        t_ids = []
        child_ids = self.list[0]['child_ids']

        while child_ids:
            within = set([])
            for c_id in child_ids:
                C = self.list[c_id]

                if edge_ids[0] in C['vtx_ids'] and edge_ids[1] in C['vtx_ids']:
                    within.add(c_id)
                elif edge_ids[0] in C['vtx_ids'] or edge_ids[1] in C['vtx_ids']:
                    p_id = set(edge_ids) - set(C['vtx_ids'])
                    p_id = next(iter(p_id))
                    if p_id == -2:
                        p = self.P_2
                    elif p_id == -1:
                        p = self.P_1
                    else:
                        p = self.P[p_id]
                    if triangles_helper.is_inside(C, p, self.P):
                        within.add(c_id)
                else:
                    if edge_ids[0] == -2:
                        p1 = self.P_2
                    elif edge_ids[0] == -1:
                        p1 = self.P_1
                    else:
                        p1 = self.P[edge_ids[0]]

                    if edge_ids[1] == -2:
                        p2 = self.P_2
                    elif edge_ids[1] == -1:
                        p2 = self.P_1
                    else:
                        p2 = self.P[edge_ids[1]]

                    if triangles_helper.is_inside(C, p1, self.P) \
                        and triangles_helper.is_inside(C, p2, self.P):
                        within.add(c_id)

            child_ids = []
            for t_id in within:
                if self.list[t_id]['child_ids']:
                    child_ids += self.list[t_id]['child_ids']
                else:
                    if edge_ids[0] in self.list[t_id]['vtx_ids'] and edge_ids[1] in self.list[t_id]['vtx_ids']:
                        t_ids.append(t_id)

        return t_ids

    def flip(self, T, T_nb, point, point_nb, edge):
        T1 = self.add(
            [point['id'], point_nb['id'], edge[0]['id']],
            [T['id'], T_nb['id']], []
        )

        T2 = self.add(
            [point['id'], point_nb['id'], edge[1]['id']],
            [T['id'], T_nb['id']], []
        )

        T['child_ids'] += [T1['id'], T2['id']]
        T_nb['child_ids'] += [T1['id'], T2['id']]

        return [edge[0]['id'], point_nb['id']], [edge[1]['id'], point_nb['id']], T1, T2

    def legalize(self, point, edge_ids, T):
        if self.P_1['id'] in T['vtx_ids'] and self.P_2['id'] in T['vtx_ids']:
            return

        if self.P_1['id'] in T['vtx_ids'] and self.P[-1]['id'] in T['vtx_ids']:
            return

        if self.P_2['id'] in T['vtx_ids'] and self.P[-1]['id'] in T['vtx_ids']:
            return

        if point['id'] < 0 and any(edge_ids) < 0 and point['id'] < min(edge_ids):
            return

        t_nb_ids = self.find_neighbour_sharing_edge(edge_ids)

        if len(t_nb_ids) != 2 or T['id'] not in t_nb_ids:
            print('I should not be here!')
            sys.exit()

        T_nb_id = set(t_nb_ids) - {T['id']}
        T_nb_id = next(iter(T_nb_id))
        T_nb = self.list[T_nb_id]

        point_nb_id = set(T_nb['vtx_ids']) - set(edge_ids)
        point_nb_id = next(iter(point_nb_id))
        if point_nb_id == -2:
            point_nb = self.P_2
        elif point_nb_id == -1:
            point_nb = self.P_1
        else:
            point_nb = self.P[point_nb_id]

        if all(edge_ids) > 0 and point['id'] > 0 and point_nb['id'] < 0:
            return

        if point['id'] > 0 and any(edge_ids) < 0 and point_nb['id'] < min(edge_ids):
            return

        edge = []
        for eid in edge_ids:
            if eid == -2:
                edge.append(self.P_2)
            elif eid == -1:
                edge.append(self.P_1)
            else:
                edge.append(self.P[eid])

        if point['id'] < 0 and any(edge_ids) < 0 and point['id'] > min(edge_ids):
            new_edge_1, new_edge_2, T1, T2 = self.flip(
                T, T_nb, point, point_nb, edge)

            self.legalize(point, new_edge_1, T1)
            self.legalize(point, new_edge_2, T2)

        elif all(edge_ids) > 0 and point['id'] > 0 and point_nb['id'] > 0:
            e1 = self.P[edge_ids[0]]
            e2 = self.P[edge_ids[1]]

            if points_helper.det(point, e1, e2) < 0:  # clockwise
                in_circle = points_helper.det_circle(
                    point, e1, e2, point_nb)
            else:
                in_circle = points_helper.det_circle(
                    point, e2, e1, point_nb)

            if in_circle > 0:
                new_edge_1, new_edge_2, T1, T2 = self.flip(
                    T, T_nb, point, point_nb, edge)

                self.legalize(point, new_edge_1, T1)
                self.legalize(point, new_edge_2, T2)

        elif point['id'] > 0 and any(edge_ids) < 0:
            if point_nb['id'] > min(edge_ids):
                new_edge_1, new_edge_2, T1, T2 = self.flip(
                    T, T_nb, point, point_nb, edge)

                self.legalize(point, new_edge_1, T1)
                self.legalize(point, new_edge_2, T2)
        else:
            print('I should not be here!')

    def leaves(self):
        l = []
        for t in self.list.values():
            if not t['child_ids'] and self.P_1['id'] not in t['vtx_ids'] and self.P_2['id'] not in t['vtx_ids']:
                l.append(t)

        return l