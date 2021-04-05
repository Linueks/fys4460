import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
from skimage.measure import label, regionprops
plt.style.use('ggplot')



def density_of_spanning_clusters(p, system_shape = (10, 10)):
    """
    Calculates P(p, L), passing in a shape for L in case I want to make
    systems that are not squares. Here p is the probability of a site
    (or however you say it)

    If something percolates a system it means that we are able to walk from one
    side to the other along a path connected by manhattan distance.
    """

    system = np.random.rand(system_shape[0], system_shape[1]) < p
    #print(system)
    labels, num = label(system, return_num=True, connectivity=1)
    #print(np.unique(labels, return_counts=True))
    props = regionprops(labels)
    #print(props)
    #print(np.unique(props, return_counts=True))

    n_percolating = 0
    percolating_area = 0

    for prop in props:
        #print(prop.area)
        row_min, col_min, row_max, col_max = prop.bbox

        if row_max - row_min == system_shape[0]\
        or col_max - col_min == system_shape[1]:
            n_percolating += 1
            percolating_area += prop.area


    total_area = system_shape[0] * system_shape[1]

    return percolating_area / (total_area)#, n_percolating



if __name__=='__main__':
    np.random.seed(1337)

    number_of_systems = 10
    probabilities = np.linspace(0, 1, number_of_systems)
    #system_sizes = np.array([1, 2, 10, 100, 500])
    system_sizes = np.array([50, 100, 200, 300, 500])
    fig, ax = plt.subplots(figsize=(16, 10))
    print(system_sizes)

    for l in system_sizes:
        print(l)
        densities = np.zeros(len(probabilities))
        n_percolating_systems = 0
        #print(l)
        for i in range(number_of_systems):
            p = probabilities[i]
            #print(p)
            """densities[i], n_percolating = density_of_spanning_clusters(p,
                                                system_shape = (l, l))"""
            densities[i] = density_of_spanning_clusters(p, system_shape=(l, l))
            #n_percolating_systems += n_percolating > 0

        ax.plot(probabilities, densities, label=f'$L = {l}$')

    plt.legend()
    plt.xlabel('$p$')
    plt.ylabel('$P(p, L)$')
    plt.title('Density of Spanning Clusters for varying system size')
    plt.show()
