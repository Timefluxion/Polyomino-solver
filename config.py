from enum import Enum


class PolyominoShapes(Enum):
    RECT = 0,
    CUBE = 1,
    U = 2


ROTATIONS = [
    lambda coord: (coord[0], coord[1]),    # 0    (x, y) => (x, y)
    lambda coord: (-coord[1], coord[0]),   # 90   (x, y) => (-y, x)
    lambda coord: (-coord[0], -coord[1]),  # 180  (x, y) => (-x, -y)
    lambda coord: (coord[1], -coord[0])    # 270  (x, y) => (y, -x)
]
