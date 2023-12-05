import random

import pandas as pd
from time import perf_counter
from utils._logging import logger


class TSPGeneticAlgorithm:
    def __init__(
        self,
        distance_matrix,
        population_size=50,
        elite_size=10,
        mutation_rate=0.01,
        generations=500,
    ):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def calculate_distance(self, route):
        total_distance = 0
        for i in range(self.num_cities - 1):
            city1 = route[i]
            city2 = route[i + 1]
            total_distance += self.distance_matrix.loc[city1, city2]
        total_distance += self.distance_matrix.loc[
            route[-1], route[0]
        ]  # Return to the starting city
        return total_distance

    def create_individual(self):
        return random.sample(range(self.num_cities), self.num_cities)

    def create_initial_population(self):
        return [self.create_individual() for _ in range(self.population_size)]

    def rank_routes(self, population):
        return sorted(population, key=lambda x: self.calculate_distance(x))

    def select_parents(self, ranked_population):
        parents = []
        for i in range(self.elite_size):
            parents.append(ranked_population[i])
        for i in range(self.population_size - self.elite_size):
            parents.append(self.tournament_selection(ranked_population))
        return parents

    def tournament_selection(self, population):
        tournament_size = 5
        tournament = random.sample(population, tournament_size)
        return min(tournament, key=lambda x: self.calculate_distance(x))

    def crossover(self, parent1, parent2):
        crossover_point1 = random.randint(0, self.num_cities - 1)
        crossover_point2 = random.randint(crossover_point1 + 1, self.num_cities)
        child = [None] * self.num_cities
        child[crossover_point1:crossover_point2] = parent1[
            crossover_point1:crossover_point2
        ]
        remaining_cities = [city for city in parent2 if city not in child]
        index = 0
        for i in range(self.num_cities):
            if child[i] is None:
                child[i] = remaining_cities[index]
                index += 1
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            mutation_point1 = random.randint(0, self.num_cities - 1)
            mutation_point2 = random.randint(0, self.num_cities - 1)
            individual[mutation_point1], individual[mutation_point2] = (
                individual[mutation_point2],
                individual[mutation_point1],
            )
        return individual

    def evolve_population(self, current_population):
        ranked_population = self.rank_routes(current_population)
        parents = self.select_parents(ranked_population)
        children = []
        while len(children) < self.population_size - self.elite_size:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            children.append(self.mutate(child))
        return parents + children

    def genetic_algorithm(self):
        current_population = self.create_initial_population()
        for generation in range(self.generations):
            logger.info(f"Generation: {generation}")
            current_population = self.evolve_population(current_population)
        best_route = self.rank_routes(current_population)[0]
        best_distance = self.calculate_distance(best_route)
        return best_route, best_distance
