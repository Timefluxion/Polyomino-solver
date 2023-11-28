from typing import Tuple, List, Set
from itertools import product

from .polyomino import Polyomino
import config


class PolyominoConstructor:
    def construct_all(self, rect_shaped_polyominoes: List[Tuple[Tuple[int, int], int]],
                      u_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]) -> List[Polyomino]:
        """
        Строит все полиомино заданных форм.

        :param rect_shaped_polyominoes: Список параметров прямоугольных полиомино.
        :type rect_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]
        :param u_shaped_polyominoes: Список параметров П-образных полиомино.
        :type u_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]
        :return: Список конструированных полиомино.
        :rtype: List[Polyomino]
        """
        constructed_polyominoes = list()
        # Строим прямоугольные полиомино
        for (height, width), count in rect_shaped_polyominoes:
            constructed_polyominoes += [Polyomino(width, height,
                                                  self.__construct_polyomino(width, height, shape=config.PolyominoShapes.RECT),
                                                  config.PolyominoShapes.RECT) for _ in range(count)]
        # Строим П-образные полиомино
        for (height, width), count in u_shaped_polyominoes:
            constructed_polyominoes += [Polyomino(width, height,
                                                  self.__construct_polyomino(width, height, shape=config.PolyominoShapes.U),
                                                  config.PolyominoShapes.U) for _ in range(count)]
        return constructed_polyominoes

    @staticmethod
    def __construct_polyomino(width: int, height: int, shape: config.PolyominoShapes) -> Set[Tuple[int, int]]:
        """
        Строит полиомино заданной формы.

        :param width: Ширина полиомино.
        :type width: int
        :param height: Высота полиомино.
        :type height: int
        :param shape: Форма полиомино (Прямоугольный или П-образный.
        :type shape: PolyominoShapes
        :return: Множество координат блоков полиомино.
        :rtype: Set[Tuple[int, int]]
        """
        coords = set()
        for x in range(width):
            coords.add((x, 0))
        for y, x in product(range(1, height),
                            range(0, width, width - 1 if shape == config.PolyominoShapes.U else 1)):
            coords.add((x, y))
        return coords
