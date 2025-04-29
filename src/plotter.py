import matplotlib.pyplot as plt

def plot_tour(coords, route, filename=None, title="Best Route", fig=None):
    x = [coords[i][0] for i in route + [route[0]]]
    y = [coords[i][1] for i in route + [route[0]]]
    if fig is None:
        fig = plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(title)
    if filename:
        plt.savefig(filename)
        plt.close()

def plot_convergence(data, filename=None, title="Convergence", fig=None):
    if fig is None:
        fig = plt.figure()
    plt.plot(data)
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("Distance")
    if filename:
        plt.savefig(filename)
        plt.close()
