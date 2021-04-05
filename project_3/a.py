import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as spi
import skimage as ski
from skimage.measure import label, regionprops

plt.style.use('ggplot')



def density_of_spanning_clusters(p, samples=1, system_shape = (10, 10)):
    """
    Calculates P(p, L), passing in a shape for L in case I want to make
    systems that are not squares. Here p is the probability of a site
    (or however you say it)

    If something percolates a system it means that we are able to walk from one
    side to the other along a path connected by manhattan distance.
    """

    system = np.random.rand(system_shape[0], system_shape[1])
    labels, num = label(system, return_num=True, connectivity=1)
    props = regionprops(labels)

    n_percolating = 0
    percolating_area = 0

    for i in range(samples):
        for prop in props:
            row_min, col_min, row_max, col_max = prop.bbox

            if row_max - row_min == system_shape[0]\
            or col_max - col_min == system_shape[1]:
                n_percolating += 1
                percolating_area += prop.area


        total_area = system_shape[0] * system_shape[1]


    return percolating_area / (total_area), n_percolating



if __name__=='__main__':
    np.random.seed(1337)
    density_of_spanning_clusters(0.5)

    number_of_systems = 100
    probabilities = np.linspace(0, 1, number_of_systems)
    #system_sizes = np.array([1, 2, 10, 100, 500])
    system_sizes = np.array([50, 100, 200, 300, 500])

    fig, ax = plt.subplots(figsize=(16, 10))

    for l in system_sizes:
        densities = np.zeros(len(probabilities))
        n_percolating_systems = 0

        for i in range(number_of_systems):
            p = probabilities[i]
            densities[i], n_percolating = density_of_spanning_clusters(p,
                                                system_shape = (l, l))
            n_percolating_systems += n_percolating > 0

        ax.plot(probabilities, densities, label=f'$L = {l}$')

    plt.legend()
    plt.xlabel('$p$')
    plt.ylabel('$P(p, L)$')
    plt.title('Density of Spanning Clusters for varying system size')
    plt.show()
