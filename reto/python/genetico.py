import pandas as pd
from time import perf_counter


from utils.metaheuristics.genetico import TSPGeneticAlgorithm
from utils._logging import logger


def main(red: str):
    scenario = (
        pd.read_csv(f"../datos/03_redes/{red}")
        .rename(columns={"Unnamed: 0": "index"})
        .set_index("index")
    )

    nodes = scenario.index.to_list()

    dmatrix = pd.read_csv("../datos/02_dmatrix/dmatrix.csv")
    dmatrix = dmatrix.rename(
        columns={column: int(column) for column in dmatrix.columns}
    )
    dmatrix = dmatrix.loc[nodes, nodes].reset_index(drop=True)

    dmatrix = dmatrix.rename(
        columns={column: i for i, column in enumerate(dmatrix.columns)}
    )

    population_size = 25
    elite_size = 10
    mutation_rate = 0.1
    generations = 1000

    tsp_genetic_algorithm = TSPGeneticAlgorithm(
        distance_matrix=dmatrix,
        population_size=population_size,
        elite_size=elite_size,
        mutation_rate=mutation_rate,
        generations=generations,
    )

    start = perf_counter()

    best_route, best_distance = tsp_genetic_algorithm.genetic_algorithm()

    end = perf_counter()

    print(f"=== Red: {red.split('.')[0]} ===\n")

    print("Tiempo de ejecucion:", end - start, "seconds")
    print("Mejor Ruta:", best_route + [best_route[0]])
    print("Distancia Total:", best_distance)

    print("\n")

    print("Numero de generaciones:", generations)
    print("Tamano de poblacion:", population_size)
    print("Tamano de poblacion eite", elite_size)
    print("Probabilidad de Mutacion:", mutation_rate)

    print("\n\n")


if __name__ == "__main__":
    for i in range(1, 11):
        red = f"n200/{i}.csv"
        start = perf_counter()
        main(red=red)
        end = perf_counter()

    logger.info(f"\nComplete Program Execution Time: {(end-start)*1000}ms\n")
