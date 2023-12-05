import numpy as np

class AntColonyOptimization:
    def __init__(self, distance_matrix, num_ants=10, max_iterations=100, alpha=1, beta=2, evaporation_rate=0.5):
        self.distance_matrix = distance_matrix
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        self.alpha = alpha  # Influencia de las feromonas
        self.beta = beta    # Influencia de la distancia
        self.evaporation_rate = evaporation_rate
        self.pheromone_matrix = np.ones_like(distance_matrix) / len(distance_matrix)
        self.best_route = None
        self.best_distance = float('inf')

    def _update_pheromones(self, ants):
        self.pheromone_matrix *= (1 - self.evaporation_rate)  # Evaporación de feromonas
        for ant in ants:
            route = ant['route']
            distance = ant['distance']
            for i in range(len(route) - 1):
                current_node, next_node = route[i], route[i + 1]
                self.pheromone_matrix[current_node][next_node] += 1 / distance
                self.pheromone_matrix[next_node][current_node] += 1 / distance

    def _get_distance(self, route):
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        return distance

    def ant_colony_optimization(self):
        for iteration in range(self.max_iterations):
            ants = []
            for _ in range(self.num_ants):
                current_node = np.random.randint(0, len(self.distance_matrix))
                visited_nodes = [current_node]
                distance_travelled = 0
                while len(visited_nodes) < len(self.distance_matrix):
                    probabilities = (self.pheromone_matrix[current_node] ** self.alpha) * \
                                    ((1 / (self.distance_matrix[current_node] + 1)) ** self.beta)
                    probabilities[visited_nodes] = 0
                    probabilities /= probabilities.sum()
                    next_node = np.random.choice(np.arange(len(self.distance_matrix)), p=probabilities)
                    distance_travelled += self.distance_matrix[current_node][next_node]
                    visited_nodes.append(next_node)
                    current_node = next_node
                distance_travelled += self.distance_matrix[visited_nodes[-1]][visited_nodes[0]]  # Regreso al inicio
                ants.append({'route': visited_nodes, 'distance': distance_travelled})

            self._update_pheromones(ants)

            # Encontrar la mejor solución actual
            for ant in ants:
                if ant['distance'] < self.best_distance:
                    self.best_distance = ant['distance']
                    self.best_route = ant['route']

        return self.best_route, self.best_distance