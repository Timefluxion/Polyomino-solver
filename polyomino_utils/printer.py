from typing import Tuple, List, Collection, Set

from pysat.formula import IDPool

from .polyomino import Polyomino
from utils import TextPainter


class PolyominoPrinter:
    def print_all(self, table_size, polyominoes: Collection[Polyomino], separate=False) -> None:
        """
        Выводит все полиомино на указанный размер таблицы.

        :param table_size: Размер таблицы (ширина, высота).
        :type table_size: Tuple[int, int]
        :param polyominoes: Коллекция полиомино для вывода.
        :type polyominoes: Collection[Polyomino]
        :param separate: Флаг, указывающий, выводить ли полиомино отдельно.
        :type separate: bool
        :return: None
        :rtype: None
        """
        text_painter = TextPainter()
        colours = [text_painter.get_random_colour() for _ in range(len(polyominoes))]
        if separate:
            for poly, colour in zip(polyominoes, colours):
                self.print_one(table_size, poly, text_painter, colour)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        else:
            table_width, table_height = table_size
            matrix = [["#"] * table_width for _ in range(table_height)]
            for poly, colour in zip(polyominoes, colours):
                for x, y in poly.coords:
                    matrix[y][x] = text_painter.get_coloured_text("*", *colour)
            for row in matrix:
                print("  ".join(row))

    def print_result_from_model(self, table_size: Tuple[int, int],
                                model: List, pool: IDPool, all_combinations: List[List[Polyomino]]) -> None:
        """
        Выводит результат модели SAT-solver'а на указанный размер таблицы.

        :param table_size: Размер таблицы (ширина, высота).
        :type table_size: Tuple[int, int]
        :param model: Список идентификаторов результата модели.
        :type model: List
        :param pool: Объект пула идентификаторов.
        :type pool: IDPool
        :param all_combinations: Список всех комбинаций полиомино.
        :type all_combinations: List[List[Set[Polyomino]]]
        :return: None
        :rtype: None
        """
        polyominoes = []
        for vid in model:
            obj = pool.obj(vid)
            if not obj:
                continue
            row_index, col_index = obj
            polyominoes.append(all_combinations[row_index][col_index])
        self.print_all(table_size, polyominoes)

    @staticmethod
    def print_one(table_size: Tuple[int, int], polyomino: Polyomino, text_painter: TextPainter, colour: Tuple[int, int, int]) -> None:
        """
        Выводит одно полиомино на указанный размер таблицы.

        :param table_size: Размер таблицы (ширина, высота).
        :type table_size: Tuple[int, int]
        :param polyomino: Полиомино для вывода.
        :type polyomino: Polyomino
        :param text_painter: Объект для покраски текста.
        :type text_painter: TextPainter
        :param colour: Цвет полиомино.
        :type colour: Tuple[int, int, int]
        :return: None
        :rtype: None
        """
        table_width, table_height = table_size
        matrix = [["#"] * table_width for _ in range(table_height)]
        for x, y in polyomino.coords:
            matrix[y][x] = text_painter.get_coloured_text("*", *colour)
        for row in matrix:
            print("  ".join(row))
