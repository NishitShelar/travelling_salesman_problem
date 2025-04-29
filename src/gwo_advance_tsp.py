import random
from src.utils import total_distance

def crossover_gwo(p1, p2):
    size = len(p1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = p1[start:end]
    p2_index = 0
    for i in range(size):
        if child[i] == -1:
            while p2[p2_index] in child:
                p2_index += 1
            child[i] = p2[p2_index]
    return child

def run_gwo_advanced(coords, num_wolves=10, iterations=100):
    n = len(coords)
    wolves = [random.sample(range(n), n) for _ in range(num_wolves)]
    fitness = [total_distance(coords, w) for w in wolves]
    alpha, beta, delta = sorted(zip(fitness, wolves))[:3]

    convergence = []

    for t in range(iterations):
        new_wolves = []
        for w in wolves:
            child = crossover_gwo(alpha[1], w)
            if random.random() < 0.3:
                i, j = sorted(random.sample(range(n), 2))
                child[i:j] = reversed(child[i:j])
            new_wolves.append(child)
        wolves = new_wolves
        fitness = [total_distance(coords, w) for w in wolves]
        alpha, beta, delta = sorted(zip(fitness, wolves))[:3]
        convergence.append(alpha[0])

    return alpha[1], alpha[0], convergence
