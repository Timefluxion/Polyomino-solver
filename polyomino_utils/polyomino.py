from typing import Set, Tuple

import config


class Polyomino:
    def __init__(self, width: int, height: int, coords: Set[Tuple[int, int]], shape: config.PolyominoShapes):
        self.coords = coords
        self.width = width
        self.height = height
        self.shape = shape

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords})"

    def __copy__(self):
        return Polyomino(self.width, self.height, self.coords.copy(), self.shape)

    # для проверки пересечения используя такой же синтаксис как у множеств(set): x1 & x2
    def __and__(self, other):
        return self.coords & other.coords

    def rotate(self, n):
        self.coords = set(map(config.ROTATIONS[n], self.coords))

    # перемещает полиомино в левый верхний угол и смещает его по вектору
    def normalize_and_translate(self, offset_x, offset_y):
        min_x = self.get_min_x()
        min_y = self.get_min_y()
        self.coords = set(map(lambda coord: (coord[0] - min_x + offset_x, coord[1] - min_y + offset_y), self.coords))

    def get_min_x(self):
        min_coords = min(self.coords, key=lambda coord: coord[0])
        return min_coords[0]

    def get_min_y(self):
        min_coords = min(self.coords, key=lambda coord: coord[1])
        return min_coords[1]
