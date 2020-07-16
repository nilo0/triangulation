from .map_api.srtm3 import SRTM3API

from .helpers import points as points_helper
from .helpers import triangles as triangles_helper


class Triangulation:
    def __init__(
            self,
            number_of_points,
            bottom_left={'lat': 47.37645735, 'lon': 8.4330368},
            top_right={'lat': 47.42727336, 'lon': 8.55671103},
            testing=False):

        area = [
            bottom_left['lat'], bottom_left['lon'],
            top_right['lat'], top_right['lon']
        ]

        srtm3 = SRTM3API(area)

        # Points
        self.P = points_helper.generate_lex_order(
            number_of_points, srtm3.elevation, testing=testing)

        # Triangles (and adding the root triangle)
        self.T = [triangles_helper.new(0, [self.P[-1], -1, -2])]

    def add_triangle(self, vtx_ids, parent_ids=[], child_ids=[], nb_ids=[]):
        self.T.append(triangles_helper.new(
            len(self.T), vtx_ids,
            parent_ids=parent_ids, child_ids=child_ids, nb_ids=nb_ids))

        return self.T[-1]

    def locate(self, point):
        children_ids = self.T[0]['children']

        found = []

        while children_ids:
            within = []
            for child_id in children_ids:
                child = self.T[child_id]

                if triangles_helper.is_inside(child, point, self.P):
                    within.append(child_id)

            children_ids = []

            for i in within:
                if self.T[i]['children']:
                    children_ids += self.T[i]['children']
                else:
                    found.append(i)

        return found

    def Delaunay(self):
        for p in self.P[:-1]:

            location_ids = self.locate(p['id'])

            if len(location_ids) == 1:
                T = self.T[location_ids[0]]

                T1 = self.add_triangle(
                    [p['id'], T['vtx_ids'][0], T['vtx_ids'][1]],
                    parents=[T['id']])
                T2 = self.add_triangle(
                    [p['id'], T['vtx_ids'][0], T['vtx_ids'][2]],
                    parents=[T['id']])
                T3 = self.add_triangle(
                    [p['id'], T['vtx_ids'][1], T['vtx_ids'][2]],
                    parents=[T['id']])

                T['children'] += [T1['id'], T2['id'], T3['id']]

                self.legalize(p, [T['vtx_ids'][0], T['vtx_ids'][1]], T1)
                self.legalize(p, [T['vtx_ids'][0], T['vtx_ids'][2]], T2)
                self.legalize(p, [T['vtx_ids'][1], T['vtx_ids'][2]], T3)

            elif len(location_ids) == 2:
                TL = self.T[location_ids[0]]
                TR = self.T[location_ids[1]]

                common_vtx = triangles_helper.common_vertices(TL, TR)

                vL = set(TL['vtx_ids']) - set(common_vtx)
                vR = set(TR['vtx_ids']) - set(common_vtx)

                T1 = self.add_triangle(
                    [p['id'], common_vtx[0], vL], parent_ids=[TL['id']])
                T2 = self.add_triangle(
                    [p['id'], common_vtx[1], vL], parent_ids=[TL['id']])

                TL['child_ids'] += [T1['id'], T2['id']]

                T3 = self.add_triangle(
                    [p['id'], common_vtx[0], vR], parent_ids=[TR['id']])
                T4 = self.add_triangle(
                    [p['id'], common_vtx[1], vR], parent_ids=[TR['id']])

                TR['child_ids'] += [T3['id'], T4['id']]

                self.legalize(p, [common_vtx[0], vL], T1)
                self.legalize(p, [common_vtx[1], vL], T2)
                self.legalize(p, [common_vtx[0], vR], T3)
                self.legalize(p, [common_vtx[1], vR], T4)
            else:
                print('I should not be here!')

    def find_neighbor(self, edge):
        e1 = self.P[edge[0]['id']]
        e2 = self.P[edge[1]['id']]

        point = points_helper.new(
            lat=(e1['lat'] + e2['lat']) / 2,
            lon=(e1['lon'] + e2['lon']) / 2,
        )

        nb_ids = self.locate(point)

        assert len(nb_ids) == 2
        return nb_ids

    def flip(self, T, T_nb, point, point_nb, edge):
        T1 = self.add_triangle(
            [point['id'], point_nb['id'], edge[0]['id']],
            parents=[T['id'], T_nb['id']]
        )

        T2 = self.add_triangle(
            [point['id'], point_nb['id'], edge[1]['id']],
            parents=[T['id'], T_nb['id']]
        )

        T['child_ids'] += [T1['id'], T2['id']]
        T_nb['child_ids'] += [T1['id'], T2['id']]

        return [edge[0], point_nb], [edge[1], point_nb], T1, T2

    def legalize(self, point, edge, T):
        """
        point_id
        edge_ids := list of two node ids of the edge
        """
        if -1 in T['vtx_ids'] and -2 in T['vtx_ids']:
            return

        edge_ids = [e['id'] for e in edge]

        T_nb_id = set(self.find_neighbor(edge)) - {T['id']}
        T_nb = self.T[T_nb_id]

        point_nb_id = set(T_nb['vtx_ids']) - set([e['id'] for e in edge])

        point_ids = [point['id'], point_nb_id]

        if all(edge_ids + point_ids) > 0:
            point_nb = self.P[point_nb_id]

            if points_helper.det(point, edge[0], edge[1]) < 0:  # clockwise
                in_circle = points_helper.det_circle(
                    point, edge[0], edge[1], point_nb)
            else:
                in_circle = points_helper.det_circle(
                    point, edge[1], edge[0], point_nb)

            if in_circle > 0:
                new_edge_1, new_edge_2, _, _ = self.flip(
                    T, T_nb, point, point_nb, edge)

                self.legalize(point, new_edge_1)
                self.legalize(point, new_edge_2)

        elif set(edge_ids) < {-1, -2} \
                or set(edge_ids) == {-1, self.P[-1]['id']} \
                or set(edge_ids) == {-2, self.P[-1]['id']}:
            return

        elif all(edge_ids) > 0 and point['id'] > 0 and point_nb['id'] < 0:
            return

        elif point['id'] > 0 and any(edge_ids) < 0:
            if point_nb['id'] < min(edge_ids):
                return
            else:
                new_edge_1, new_edge_2, T1, T2 = self.flip(
                    T, T_nb, point, point_nb, edge)

                self.legalize(point, new_edge_1, T1)
                self.legalize(point, new_edge_2, T2)

        elif point['id'] < 0 and any(edge_ids) < 0:
            if point['id'] < min(edge_ids):
                return
            else:
                new_edge_1, new_edge_2, T1, T2 = self.flip(
                    T, T_nb, point, point_nb, edge)

                self.legalize(point, new_edge_1, T1)
                self.legalize(point, new_edge_2, T2)
        else:
            print('I should not be here!')
