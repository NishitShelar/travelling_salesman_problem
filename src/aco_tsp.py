import numpy as np
import random
from src.utils import total_distance, euclidean

def run_aco(coords, num_ants=10, iterations=100, alpha=1, beta=5, evaporation=0.5):
    n = len(coords)
    pheromone = np.ones((n, n))
    distance = np.array([[euclidean(coords[i], coords[j]) for j in range(n)] for i in range(n)])
    convergence = []
    best_route = None
    best_length = float('inf')

    for _ in range(iterations):
        all_routes = []
        all_lengths = []

        for _ in range(num_ants):
            route = [random.randint(0, n-1)]
            while len(route) < n:
                current = route[-1]
                probs = []
                for j in range(n):
                    if j not in route:
                        probs.append((pheromone[current][j]**alpha) * (1/distance[current][j])**beta)
                    else:
                        probs.append(0)
                probs = np.array(probs)
                probs /= probs.sum()
                next_city = np.random.choice(range(n), p=probs)
                route.append(next_city)

            length = total_distance(coords, route)
            if length < best_length:
                best_route = route
                best_length = length
            all_routes.append(route)
            all_lengths.append(length)

        pheromone *= (1 - evaporation)
        for route, length in zip(all_routes, all_lengths):
            for i in range(n):
                pheromone[route[i]][route[(i+1)%n]] += 1/length

        convergence.append(best_length)

    return best_route, best_length, convergence
