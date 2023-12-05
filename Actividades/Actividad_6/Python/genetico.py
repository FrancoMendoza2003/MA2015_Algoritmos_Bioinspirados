import pandas as pd
from time import perf_counter


from utils.heuristics import BinaryGeneticAlgorithm
from utils._logging import logger


def main():
    """
    't_i': Se tiene un tiempo de procesamiento 'ti' y
    'd_i': una fecha límite 'di' para ser realizada.

    'h_i': Si la tarea i se completa antes de la fecha límite, incurre en un costo de retención 'hi' por unidad de tiempo.
    'c_i': Una tarea retardada i da como resultado un costo de penalización 'ci' por unidad de tiempo
    """

    scenario = pd.DataFrame(
        data={
            "Job": [1, 2, 3, 4, 5],
            "t_i": [10, 8, 6, 7, 4],
            "d_i": [15, 20, 10, 30, 12],
            "h_i": [3, 2, 5, 4, 6],
            "c_i": [10, 22, 10, 8, 15],
        },
    ).set_index("Job")

    solver = BinaryGeneticAlgorithm.from_scenario(
        scenario=scenario,
        n=20,
        only_feasable_solutions=True,
    )
    solution, exec_time = solver.solve(
        generations=1000,
        crossover_point=10,
        crossover_rate=0.9,
        mutation_rate=0.1,
    )

    logger.info(f"Costo de Solución: {solution._calculate_gene_cost()}")
    logger.info(f"Tiempo de Ejecución de Algoritmo: {exec_time*1000}ms")
    logger.info(f"Cromosoma Final: \n{solution}")
    logger.info(f"Tiempo Acumlado: \n{solution.accumulated_time}")
    logger.info(f"Costos de Retención: \n{solution.retention_cost_list}")
    logger.info(f"Costos de Penalización: \n{solution.penalization_cost_list}")


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()

    print(f"\nComplete Program Execution Time: {(end-start)*1000}ms\n")
