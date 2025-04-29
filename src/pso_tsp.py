import random
from src.utils import total_distance

def swap_sequence(p1, p2):
    seq = []
    p2_pos = {city: i for i, city in enumerate(p2)}
    for i in range(len(p1)):
        if p1[i] != p2[i]:
            swap_idx = p2_pos[p1[i]]
            seq.append((i, swap_idx))
            p2[i], p2[swap_idx] = p2[swap_idx], p2[i]
            p2_pos[p2[i]] = i
            p2_pos[p2[swap_idx]] = swap_idx
    return seq

def apply_swap(route, seq):
    new_route = route.copy()
    for i, j in seq:
        new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def run_pso(coords, num_particles=10, iterations=100):
    n = len(coords)
    particles = [random.sample(range(n), n) for _ in range(num_particles)]
    best_particles = particles.copy()
    best_fitness = [total_distance(coords, p) for p in particles]
    gbest = particles[best_fitness.index(min(best_fitness))]
    gbest_fitness = min(best_fitness)
    convergence = []

    for _ in range(iterations):
        for i in range(num_particles):
            swap_seq = swap_sequence(particles[i], gbest)
            particles[i] = apply_swap(particles[i], swap_seq[:5])
            new_fitness = total_distance(coords, particles[i])
            if new_fitness < best_fitness[i]:
                best_particles[i] = particles[i]
                best_fitness[i] = new_fitness
        gbest = best_particles[best_fitness.index(min(best_fitness))]
        gbest_fitness = min(best_fitness)
        convergence.append(gbest_fitness)

    return gbest, gbest_fitness, convergence
