class Polygon:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def split_coordinates(self):
        return list(zip(*self.coordinates))

    def get_concave_vertex(self):

