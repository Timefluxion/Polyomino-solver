from typing import Tuple, List
from itertools import chain
from functools import reduce

from .polyomino import Polyomino


class PolyominoValidator:
    @staticmethod
    def is_all_polyominoes_fits_table(table_size: Tuple[int, int],
                                      rect_shaped_polyominoes: List[Tuple[Tuple[int, int], int]],
                                      u_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]) -> bool:
        """
        Проверяет, что все полиомино подходят для размещения на таблице.

        :param table_size: Размер таблицы (ширина, высота).
        :type table_size: Tuple[int, int]
        :param rect_shaped_polyominoes: Список прямоугольных полимино.
        :type rect_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]
        :param u_shaped_polyominoes: Список П-образных полимино.
        :type u_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]
        :return: True, если все полиомино подходят для размещения на таблице, иначе False.
        :rtype: bool
        """
        table_width, table_height = table_size
        return all(map(
            lambda coord: not (
                    (coord[0][0] > table_width or coord[0][1] > table_height) and
                    (coord[0][1] > table_width or coord[0][0] > table_height)
            ),
            chain(rect_shaped_polyominoes, u_shaped_polyominoes)))

    @staticmethod
    def is_all_polyominoes_blocks_count_fits_table(table_size: Tuple[int, int],
                                                   polyominoes: List[Polyomino]):
        """
        Проверяет, что общее количество блоков во всех полиомино влезает в таблицу.

        :param table_size: Размер таблицы (ширина, высота).
        :type table_size: Tuple[int, int]
        :param polyominoes: Список полиомино.
        :type polyominoes: List[Polyomino]
        :return: True, если общее количество блоков во всех полиомино влезает в таблицу, иначе False.
        :rtype: bool
        """
        blocks_count = reduce(lambda total_len, poly: total_len + len(poly.coords), polyominoes, 0)
        return table_size[0] * table_size[1] >= blocks_count
