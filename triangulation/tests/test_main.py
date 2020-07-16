from ..main import Triangulation


def test_main():
    t = Triangulation(7, testing=True)
    t.Delaunay()
