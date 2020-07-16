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

    def add_triangle(self, vertices_ids, parent_ids=[], child_ids=[]):
        self.T.append(triangles_helper.new(
            len(self.T), vertices_ids,
            parent_ids=parent_ids, child_ids=child_ids))

    def locate(self, point_id):
        point = self.P[point_id]
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
