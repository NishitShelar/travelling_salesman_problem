import random
from src.utils import total_distance

def run_gwo_basic(coords, num_wolves=10, iterations=100):
    n = len(coords)
    wolves = [random.sample(range(n), n) for _ in range(num_wolves)]
    fitness = [total_distance(coords, w) for w in wolves]
    alpha, beta, delta = sorted(zip(fitness, wolves))[:3]

    convergence = []

    for t in range(iterations):
        new_wolves = []
        for w in wolves:
            i, j = sorted(random.sample(range(n), 2))
            new = w[:i] + list(reversed(w[i:j])) + w[j:]
            new_wolves.append(new)
        wolves = new_wolves
        fitness = [total_distance(coords, w) for w in wolves]
        alpha, beta, delta = sorted(zip(fitness, wolves))[:3]
        convergence.append(alpha[0])

    return alpha[1], alpha[0], convergence
