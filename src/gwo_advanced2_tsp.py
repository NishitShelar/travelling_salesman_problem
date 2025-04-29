import random
import numpy as np
from src.utils import total_distance

# === 2-opt local search ===
def two_opt(route, coords, max_improvements=3):
    count = 0
    improved = True
    while improved and count < max_improvements:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                if total_distance(coords, new_route) < total_distance(coords, route):
                    route = new_route
                    improved = True
                    count += 1
                    if count >= max_improvements:
                        return route
    return route

# === Elite Archive ===
class EliteArchive:
    def __init__(self, max_size=5):
        self.archive = []
        self.max_size = max_size

    def add(self, route, dist):
        for r, d in self.archive:
            if len(set(r) & set(route)) > 0.9 * len(route):
                return  # too similar
        self.archive.append((route[:], dist))
        self.archive.sort(key=lambda x: x[1])
        if len(self.archive) > self.max_size:
            self.archive = self.archive[:self.max_size]

    def get_random(self):
        return random.choice(self.archive)[0] if self.archive else None

# === Edge frequency memory ===
def update_edge_matrix(edge_matrix, route):
    for i in range(len(route)):
        a = route[i]
        b = route[(i + 1) % len(route)]
        edge_matrix[a][b] += 1
        edge_matrix[b][a] += 1

def build_from_edges(edge_matrix, n):
    visited = set()
    route = [random.randint(0, n - 1)]
    visited.add(route[0])
    while len(route) < n:
        last = route[-1]
        next_city = sorted([(i, edge_matrix[last][i]) for i in range(n) if i not in visited],
                           key=lambda x: -x[1])
        if next_city:
            route.append(next_city[0][0])
            visited.add(next_city[0][0])
        else:
            remaining = [i for i in range(n) if i not in visited]
            route.append(random.choice(remaining))
            visited.add(route[-1])
    return route

# === Main GWO Advanced 2.0 ===
def run_gwo_advanced2(coords, num_wolves=10, iterations=100):
    n = len(coords)
    wolves = [random.sample(range(n), n) for _ in range(num_wolves)]
    fitness = [total_distance(coords, w) for w in wolves]
    alpha, beta, delta = sorted(zip(fitness, wolves))[:3]

    edge_matrix = np.ones((n, n))  # edge frequency memory
    elite = EliteArchive()

    convergence = []

    for t in range(iterations):
        a = 2 - t * (2 / iterations)
        new_wolves = []
        for i in range(num_wolves):
            base = wolves[i]
            # Leader crossover
            c1 = crossover_segments(base, alpha[1])
            c2 = crossover_segments(c1, beta[1])
            c3 = crossover_segments(c2, delta[1])
            # Build from edges + local search every few steps
            guided = build_from_edges(edge_matrix, n)
            improved = two_opt(c3 if t % 5 != 0 else guided, coords)
            new_wolves.append(improved)

        wolves = new_wolves
        fitness = [total_distance(coords, w) for w in wolves]
        alpha, beta, delta = sorted(zip(fitness, wolves))[:3]
        convergence.append(alpha[0])

        update_edge_matrix(edge_matrix, alpha[1])
        elite.add(alpha[1], alpha[0])

        # Every 10 steps reintroduce an elite
        if t % 10 == 0 and elite.archive:
            wolves[random.randint(0, num_wolves - 1)] = elite.get_random()

    return alpha[1], alpha[0], convergence

# === Helper: segment-wise crossover ===
def crossover_segments(p1, p2):
    size = len(p1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = p1[start:end]
    fill = [city for city in p2 if city not in child]
    idx = 0
    for i in range(size):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return child
