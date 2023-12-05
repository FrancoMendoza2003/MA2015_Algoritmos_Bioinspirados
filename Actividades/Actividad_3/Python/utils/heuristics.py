from dataclasses import dataclass
from numbers import Number
from copy import deepcopy
from time import perf_counter

from utils.logging import logger


@dataclass
class Node:
    name: str | int
    cost: Number
    benefit: Number


class GreedyHeuristic:
    def __init__(self, nodes: dict[str, Node], max_cost: Number) -> None:
        self.current_cost: Number = 0
        self.current_benefit: Number = 0
        self.visited_nodes = list()

        self.nodes = nodes
        self.unvisited_nodes = nodes

        self.max_cost = max_cost

    @classmethod
    def from_values(
        cls,
        names: list[str | int],
        costs: list[Number],
        benefits: list[Number],
        max_cost: Number,
    ):
        nodes = {
            name: Node(name, cost, benefit)
            for name, cost, benefit, in zip(names, costs, benefits)
        }

        return cls(nodes=nodes, max_cost=max_cost)

    def get_max_benefit(self, possible_nodes: dict[str, Node]) -> Node:
        return possible_nodes[
            max(possible_nodes, key=lambda node: self.nodes[node].benefit)
        ]

    def get_min_cost(self, possible_nodes: dict[str, Node]) -> Node:
        return possible_nodes[
            min(possible_nodes, key=lambda node: self.nodes[node].benefit)
        ]

    def get_possible_nodes(self) -> dict[str, Node]:
        possible_nodes = deepcopy(self.unvisited_nodes)

        for name, node in self.unvisited_nodes.items():
            if (node.cost + self.current_cost > self.max_cost) or (
                name in self.visited_nodes
            ):
                del possible_nodes[name]

        return possible_nodes

    def solve(self) -> (list[str], Number, Number, float):
        start = perf_counter()
        while self.current_cost < self.max_cost and self.unvisited_nodes:
            possible_nodes = self.get_possible_nodes()

            if not possible_nodes:
                break

            best_node = self.get_max_benefit(possible_nodes)

            self.visited_nodes.append(best_node)
            self.unvisited_nodes.pop(best_node.name)

            self.current_cost += best_node.cost
            self.current_benefit += best_node.benefit

        self.print_solution()

        end = perf_counter()
        exec_time = end - start

        return self.visited_nodes, self.current_benefit, self.current_cost, exec_time

    def print_solution(self):
        solution = [node.name for node in self.visited_nodes]

        print("\nSOLUTION:\n------")
        for i, node in enumerate(solution, start=1):
            if i != len(solution):
                print(f"{node} --> ", end="")
            else:
                print(node)

        print(f"\nFunción Objetivo: {self.current_benefit}")
        print(f"Costo Total: {self.current_cost}\n")
