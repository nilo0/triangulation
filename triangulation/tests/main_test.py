from ..main import Triangulation


def test_Triangulation():
    t = Triangulation(7, testing=False)
    leaves = t.Delaunay()

    print(leaves)
