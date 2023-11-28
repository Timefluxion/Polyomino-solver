from typing import List, Tuple

from pysat.solvers import Solver
from pysat.formula import IDPool

from polyomino_utils import PolyominoConstructor, PolyominoValidator, PolyominoSolver, PolyominoPrinter


def main(table_size: Tuple[int, int],
         rect_shaped_polyominoes: List[Tuple[Tuple[int, int], int]],
         u_shaped_polyominoes: List[Tuple[Tuple[int, int], int]]) -> None:

    polyomino_validator = PolyominoValidator()
    # Проверяем, что все полиомино подходят для размещения на таблице
    if not polyomino_validator.is_all_polyominoes_fits_table(table_size, rect_shaped_polyominoes, u_shaped_polyominoes):
        print(False)
        return

    # Собираем все полиомино
    polyomino_constructor = PolyominoConstructor()
    polyominoes = polyomino_constructor.construct_all(rect_shaped_polyominoes, u_shaped_polyominoes)

    # Проверяем, что общее количество блоков во всех полиомино влезает в таблицу.
    if not polyomino_validator.is_all_polyominoes_blocks_count_fits_table(table_size, polyominoes):
        print(False)
        return

    polyomino_solver = PolyominoSolver(table_size, polyominoes)
    all_combinations = polyomino_solver.generate_all_combination()
    pool = IDPool()
    formula = polyomino_solver.generate_sat_formula(all_combinations, pool)

    solver = Solver(bootstrap_with=formula)
    is_solution_exists = solver.solve()
    print(is_solution_exists)
    if not is_solution_exists:
        return

    polyomino_printer = PolyominoPrinter()
    polyomino_printer.print_result_from_model(table_size, solver.get_model(), pool, all_combinations)


if __name__ == "__main__":
    table_size = (4, 6)
    rect_shaped_polyominoes = [((2, 2), 2)]
    u_shaped_polyominoes = [((3, 4), 1), ((2, 3), 1)]

    main(table_size, rect_shaped_polyominoes, u_shaped_polyominoes)
