import pandas as pd
from time import perf_counter


from python.utils.metaheuristics.AntColonyOptimization import AntColonyOptimization
from python.utils._logging import logger


def main(red: str):
    scenario = (
        pd.read_csv(f"datos/03_redes/{red}")
        .rename(columns={"Unnamed: 0": "index"})
        .set_index("index")
    )

    nodes = scenario.index.to_list()

    dmatrix = pd.read_csv("datos/02_dmatrix/dmatrix.csv")
    dmatrix = dmatrix.rename(
        columns={column: int(column) for column in dmatrix.columns}
    )
    dmatrix = dmatrix.loc[nodes, nodes].reset_index(drop=True)

    dmatrix = dmatrix.rename(
        columns={column: i for i, column in enumerate(dmatrix.columns)}
    )

    num_ants = 4
    max_iterations = 100
    alpha = 1
    beta = 2
    evaporation_rate = 0.5

    ant_colony_optimization = AntColonyOptimization(
        distance_matrix=dmatrix,
        num_ants=num_ants,
        max_iterations=max_iterations,
        alpha=alpha,
        beta=beta,
        evaporation_rate=evaporation_rate,
    )

    start = perf_counter()

    best_route, best_distance = ant_colony_optimization.ant_colony_optimization()

    end = perf_counter()

    print(f"=== Red: {red.split('.')[0]} ===\n")

    print("Tiempo de ejecucion:", end - start, "seconds")
    print("Mejor Ruta:", best_route + [best_route[0]])
    print("Distancia Total:", best_distance)

    print("\n")

    print("Número de iteraciones:", max_iterations)
    print("Número de hormigas:", num_ants)
    print("Alpha:", alpha)
    print("Beta:", beta)
    print("Tasa de evaporación de feromonas:", evaporation_rate)

    print("\n\n")

if __name__ == "__main__":
    for i in range(1, 11):
        red = f"n200/{i}.csv"
        start = perf_counter()
        main(red=red)
        end = perf_counter()

    logger.info(f"\nComplete Program Execution Time: {(end-start)*1000}ms\n")