import random
from src.utils import total_distance

def crossover(p1, p2):
    start, end = sorted(random.sample(range(len(p1)), 2))
    child = [-1] * len(p1)
    child[start:end] = p1[start:end]
    p2_index = 0
    for i in range(len(p1)):
        if child[i] == -1:
            while p2[p2_index] in child:
                p2_index += 1
            child[i] = p2[p2_index]
    return child

def mutate(route):
    i, j = sorted(random.sample(range(len(route)), 2))
    route[i:j] = reversed(route[i:j])
    return route

def run_ga(coords, population_size=10, generations=100):
    n = len(coords)
    pop = [random.sample(range(n), n) for _ in range(population_size)]
    convergence = []

    for _ in range(generations):
        pop = sorted(pop, key=lambda x: total_distance(coords, x))
        new_pop = pop[:2]
        while len(new_pop) < population_size:
            p1, p2 = random.choices(pop[:5], k=2)
            child = crossover(p1, p2)
            if random.random() < 0.2:
                child = mutate(child)
            new_pop.append(child)
        pop = new_pop
        convergence.append(total_distance(coords, pop[0]))

    return pop[0], total_distance(coords, pop[0]), convergence
