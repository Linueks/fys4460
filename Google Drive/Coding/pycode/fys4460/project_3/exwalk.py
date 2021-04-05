
from scipy.ndimage import measurements
from walk import walk
import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
from skimage.measure import label, regionprops
from scipy.stats import linregress
plt.style.use('ggplot')

np.random.seed(1337)



def run_walkers(width, height, n_samples, show_plot=True):
    p = 0.586
    ncount = 0
    percolating = []
    mass = np.zeros(n_samples)
    for i in range(n_samples):
        while (len(percolating)==0):
            ncount = ncount + 1
            if (ncount >1000):
                print("Couldn't make percolation cluster...")
                break

            system = np.random.rand(width, height) < p
            labels, num = label(system, return_num=True, connectivity=1)
            percolating_x = np.intersect1d(labels[0, :], labels[-1, :])
            percolating = percolating_x[percolating_x > 0]
            print(ncount)



        if len(percolating) > 0:
            label_list = np.arange(num + 1)
            area = measurements.sum(system, labels, index=label_list)
            area_image = area[labels]
            max_area = area.max()
            largest_spanning_cluster = (labels == percolating[0])
            left, right = walk(largest_spanning_cluster)

            singly_connected_mass = np.sum((left * right) > 0)
            mass[i] = singly_connected_mass
            if show_plot:
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8 , 5))

                image1 = ax1.imshow(area_image, interpolation='nearest', origin='upper', cmap='jet')
                colorbar = fig.colorbar(image1, ax=ax1)
                ax1.set_title('Plot of Clusters')

                image2 = ax2.imshow(largest_spanning_cluster, interpolation='nearest', origin='upper', cmap='jet') # Display spanning cluster
                colorbar = fig.colorbar(image2, ax=ax2)
                ax2.set_title('Largest Spanning Cluster')

                #% Run walk on this cluster
                image3 = ax3.imshow(left, interpolation='nearest', origin='upper', cmap='jet')
                colorbar = fig.colorbar(image3, ax=ax3)
                ax3.set_title('Left walker')
                image4 = ax4.imshow(right, interpolation='nearest', origin='upper', cmap='jet')
                colorbar = fig.colorbar(image4, ax=ax4)
                ax4.set_title('Right walker')

                plt.tight_layout()
                plt.show()


    return mass, largest_spanning_cluster

if __name__=='__main__':
    width = 100
    height = 100
    num_samples = 1


    L = np.power(2, np.arange(4, 11, 1))
    masses = np.zeros_like(L)

    for i, l in enumerate(L):
        print(i, l)
        mass, spanning_cluster = run_walkers(l, l, num_samples, show_plot=False)
        masses[i] = np.mean(mass)


    reg = linregress(np.log(L), np.log(masses))

    print(reg.slope, reg.intercept)

    np.save('masses.npy', masses)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(L, masses, label='Measured Mass')
    ax.loglog(L, np.exp(reg.intercept) * L**reg.slope, label=f'Estimated $D = {np.round(reg.slope, 2)}$, $exp(C) = {np.round(np.exp(reg.intercept), 2)})$')


    ax.set_xlabel('Log(L)')
    ax.set_ylabel('$Log(M)$')
    ax.set_title('Singly connected masses')
    ax.legend()
    plt.show()
