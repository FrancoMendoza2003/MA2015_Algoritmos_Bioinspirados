from time import perf_counter

from utils.heuristics import GreedyHeuristic


def main():
    names = [f"c{i}" for i in range(1, 11)]
    costs = [100, 155, 50, 112, 70, 80, 60, 118, 110, 55]
    benefits = [1741, 1622, 1016, 1264, 1305, 1389, 1797, 1330, 1559, 1578]

    benefits_ = (
        "174100	251410	50800	141568	91350	111120	107820	156940	171490	86790".split("\t")
    )
    benefits_ = [int(b) for b in benefits_]

    solver = GreedyHeuristic.from_values(
        names=names,
        costs=costs,
        benefits=benefits_,
        max_cost=700,
    )
    solver.solve()


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()

    print(f"\nExecution Time: {(end-start)*1000}ms\n")
