from .triangle import Triangle
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
        self.P_1 = points_helper.new(0, 0, id=-1)
        self.P_2 = points_helper.new(0, 0, id=-2)
        self.P = points_helper.generate_lex_order(
            number_of_points, area, srtm3.elevation, testing=testing)

        # Triangles (and adding the root triangle)
        self.T = Triangle(self.P_1, self.P_2, self.P)

    def Delaunay(self):
        for p in self.P[:-1]:

            location_ids = self.T.locate(p)

            if len(location_ids) == 1:
                T = self.T.list[location_ids[0]]

                T1 = self.T.add([p['id'], T['vtx_ids'][0], T['vtx_ids'][1]], [T['id']], [])
                T2 = self.T.add([p['id'], T['vtx_ids'][0], T['vtx_ids'][2]], [T['id']], [])
                T3 = self.T.add([p['id'], T['vtx_ids'][1], T['vtx_ids'][2]], [T['id']], [])

                self.T.list[location_ids[0]]['child_ids'].append(T1['id'])
                self.T.list[location_ids[0]]['child_ids'].append(T2['id'])
                self.T.list[location_ids[0]]['child_ids'].append(T3['id'])

                self.T.legalize(p, [T['vtx_ids'][0], T['vtx_ids'][1]], T1)
                self.T.legalize(p, [T['vtx_ids'][0], T['vtx_ids'][2]], T2)
                self.T.legalize(p, [T['vtx_ids'][1], T['vtx_ids'][2]], T3)

            elif len(location_ids) == 2:
                TL = self.T.list[location_ids[0]]
                TR = self.T.list[location_ids[1]]

                common_vtx = triangles_helper.common_vertices(TL, TR)

                vL = next(iter(set(TL['vtx_ids']) - set(common_vtx)))
                vR = next(iter(set(TR['vtx_ids']) - set(common_vtx)))

                T1 = self.T.add([p['id'], common_vtx[0], vL], [TL['id']], [])
                T2 = self.T.add([p['id'], common_vtx[1], vL], [TL['id']], [])

                TL['child_ids'].append(T1['id'])
                TL['child_ids'].append(T2['id'])

                T3 = self.T.add([p['id'], common_vtx[0], vR], [TR['id']], [])
                T4 = self.T.add([p['id'], common_vtx[1], vR], [TR['id']], [])

                TR['child_ids'].append(T3['id'])
                TR['child_ids'].append(T4['id'])

                self.T.legalize(p, [common_vtx[0], vL], T1)
                self.T.legalize(p, [common_vtx[1], vL], T2)
                self.T.legalize(p, [common_vtx[0], vR], T3)
                self.T.legalize(p, [common_vtx[1], vR], T4)
            else:
                print('I should not be here!')

        leaves = self.T.leaves()
        return leaves
