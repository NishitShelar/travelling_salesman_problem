import numpy as np

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def total_distance(coords, route):
    return sum(euclidean(coords[route[i]], coords[route[(i + 1) % len(route)]]) for i in range(len(route)))
