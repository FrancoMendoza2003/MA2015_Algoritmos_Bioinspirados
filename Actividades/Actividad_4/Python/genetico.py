from time import perf_counter


from utils.heuristics import BinaryGeneticAlgorithm
from utils._logging import logger


def main():
    costs = [
        61,
        58,
        92,
        50,
        108,
        83,
        93,
        101,
        54,
        50,
        72,
        51,
        100,
        108,
        91,
        112,
        66,
        58,
        110,
        73,
    ]
    benefits = [
        1100,
        1147,
        1442,
        1591,
        1078,
        1385,
        1777,
        1196,
        1753,
        1371,
        1517,
        1675,
        1193,
        1177,
        1365,
        1143,
        1314,
        1526,
        1470,
        1605,
    ]

    solver = BinaryGeneticAlgorithm.from_random(
        benefits=benefits,
        costs=costs,
        max_cost=800,
        only_feasable_solutions=False,
    )
    solution, exec_time = solver.solve(
        generations=50,
        crossover_point=10,
        crossover_rate=0.9,
        mutation_rate=0.1,
    )

    logger.info(f"Costo de Solución: {solution._calculate_gene_cost()}")
    logger.info(f"Tiempo de Ejecución de Algoritmo: {exec_time*1000}ms")
    logger.info(f"Cromosoma Final: \n{solution}")


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()

    print(f"\nComplete Program Execution Time: {(end-start)*1000}ms\n")
