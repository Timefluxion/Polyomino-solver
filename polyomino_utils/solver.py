from copy import copy
from typing import List, Set, Tuple, Generator
from collections.abc import Callable
from itertools import product

from pysat.formula import CNF, IDPool

from .polyomino import Polyomino
import config


class PolyominoSolver:
    def __init__(self, table_size: Tuple[int, int], polyominoes: List[Polyomino]):
        self.table_width, self.table_height = table_size
        self.polyominoes = polyominoes

    def generate_all_possible_positions_on_table(self, polyomino: Polyomino) -> Generator:
        """
        Генерирует полиомино во всех возможных позицих на таблице.

        :param polyomino: Полиомино для генерации позиций.
        :type polyomino: Polyomino
        :return: Генератор полиомино во всех возможных позициях на таблице.
        :rtype: Generator[Polyomino]
        """
        # Куб может быть только в одном состоянии, прямоугольник в двух, все остальные фигуры в четырёх
        for rotation_number, rotation_func in enumerate(self.get_rotations_for_polyomino(polyomino)):
            new_poly_width, new_poly_height = map(abs, rotation_func((polyomino.width, polyomino.height)))
            max_x_offset, max_y_offset = self.table_width - new_poly_width + 1, self.table_height - new_poly_height + 1
            for x_offset, y_offset in product(range(max_x_offset), range(max_y_offset)):
                same_poly = copy(polyomino)
                # Вращаем только если не куб
                if rotation_number:
                    same_poly.rotate(rotation_number)
                same_poly.normalize_and_translate(x_offset, y_offset)
                yield same_poly

    def generate_all_combination(self) -> List[List[Polyomino]]:
        """
        Генерирует все возможные комбинации позиций для каждого полиомино.

        :return: Список всех комбинаций позиций полиомино.
        :rtype: List[List[Polyomino]]
        """
        all_combinations = []
        for poly in self.polyominoes:
            all_combinations.append(list(self.generate_all_possible_positions_on_table(poly)))
        return all_combinations

    @staticmethod
    def generate_sat_formula(all_combinations: List[List[Set[Tuple[int, int]]]], pool: IDPool) -> CNF:
        """
        Генерирует формулу для решения задачи SAT (Boolean Satisfiability Problem).

        :param all_combinations: Список всех комбинаций позиций полиомино.
        :type all_combinations: List[List[Polyomino]]
        :param pool: Объект пула идентификаторов.
        :type pool: IDPool
        :return: Формула SAT.
        :rtype: CNF
        """
        formula = CNF()

        # Каждый полиомино существует только в одном положении
        for row_index in range(len(all_combinations)):
            for col_index in range(len(all_combinations[row_index])):
                for other_col_index in range(col_index + 1, len(all_combinations[row_index])):
                    formula.append(
                        [
                            -pool.id((row_index, col_index)),
                            -pool.id((row_index, other_col_index))
                        ]
                    )

        # Каждый полиомино существует как минимум в одном положении
        for row_index, row in enumerate(all_combinations):
            clause = [
                pool.id((row_index, col_index)) for col_index in range(len(row))
            ]
            formula.append(clause)

        # Каждый полиомино существует в позиции, которая не пересекается с позициями любых других полиомино
        for row_index in range(len(all_combinations)):
            for other_row_index in range(row_index + 1, len(all_combinations)):

                for col_index in range(len(all_combinations[row_index])):
                    for other_col_index in range(len(all_combinations[other_row_index])):
                        if all_combinations[row_index][col_index] & all_combinations[other_row_index][other_col_index]:
                            clause = [
                                -pool.id((row_index, col_index)),
                                -pool.id((other_row_index, other_col_index))
                            ]
                            formula.append(clause)

        return formula

    @staticmethod
    def get_rotations_for_polyomino(polyomino: Polyomino) -> List[Callable]:
        """
        Возвращает возможные варианты вращений для полиомино.

        :param polyomino: Полиомино для определения вариантов вращений.
        :type polyomino: Polyomino
        :return: Список функций вращения для полиомино.
        :rtype: List[Callable]
        """
        rotations = list()
        if polyomino.shape == config.PolyominoShapes.CUBE:
            rotations = config.ROTATIONS[:1]
        elif polyomino.shape == config.PolyominoShapes.RECT:
            rotations = config.ROTATIONS[:2]
        elif polyomino.shape == config.PolyominoShapes.U:
            rotations = config.ROTATIONS
        return rotations
