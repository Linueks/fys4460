import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
from skimage.measure import label, regionprops
from d import log_bin
from scipy.stats import linregress
plt.style.use('ggplot')

np.random.seed(2021)

def compute_cluster_area(system_shape, p):
    #system = np.random.choice([0, 1], size=system_shape, p=[1 - p, p])
    system = np.random.rand(system_shape[0], system_shape[1])
    mask = system < p
    labels, num = label(mask, return_num=True, connectivity=1)
    props = regionprops(labels)

    prop_list = []

    for p in props:
        row_min, col_min, row_max, col_max = p.bbox
        if row_max - row_min == system_shape[0] or col_max - col_min == system_shape[1]:
            continue
        prop_list.append(p)

    areas = [prop.area for prop in prop_list]

    return areas



def estimate_cluster_number_density(system_shape, M, p, mask_numerical_error=True):
    """
    from textbook:

    we estimate the cluster number density from a set of M numerical simulations
    N_s is the total number of clusters of size s measured for M simulations in
    a system size of L^d for a given value of p
    """

    area = []

    for i in range(M):
        area.extend(compute_cluster_area(system_shape, p))

    # this below line is not thought through for non-square systems
    n, s = np.histogram(area, system_shape[0]**2)

    # Logarithmic from textbook
    a = 1.3                                                                     # page 56 https://www.uio.no/studier/emner/matnat/fys/FYS4460/v21/notes/book.pdf
    logamax = np.ceil(np.log(max(s)) / np.log(a))
    logbins = a**np.arange(0, logamax, 1)
    nl, nlbins = np.histogram(area, logbins)
    ds = np.diff(logbins)
    sl = (logbins[1:] + logbins[:-1]) * 0.5
    nsl = nl / (M * system_shape[0]**2 * ds)


    if mask_numerical_error:
        mask = np.abs(nsl) > 1e-14
        return sl[mask], nsl[mask]

    else:
        return sl, nsl


if __name__ == '__main__':

    L = 100
    p_c = 0.59275
    M = 200
    a = 1.2


    """
    #f
    # first we were asked to go to p_c = 0.59275 from below
    fig, ax = plt.subplots(figsize=(8, 5))
    for p in np.linspace(p_c, 0.9, 10):
        print(p)
        ax.loglog(*estimate_cluster_number_density((L, L), M, p),
            label=f'p = {np.round(p, 5)}')


    plt.legend()
    plt.title(f'Cluster Number Density $n(s, p)$ for $p \\to {p_c}$ from above\n with M = {M}')
    plt.xlabel('s')
    plt.ylabel('$n(s, p)$')
    plt.show()

    #"""

    """
    #g
    system_sizes = 2**np.arange(4, 10, 1)

    # not so sure about this
    fig, ax = plt.subplots(figsize=(8, 5))
    for l in system_sizes:
        print(l)
        system_shape = (l, l)
        sl, nsl = estimate_cluster_number_density(system_shape, M, p_c)
        slope, intercept, r, p, se = linregress(np.log(sl) / np.log(a),
                                                np.log(nsl) / np.log(a))
        ax.loglog(sl, nsl, label=f'L = {l}, $\\tau = {np.round(slope, 2)}$')

    plt.legend()
    plt.title(f'Cluster Number Density at Critical Percolation Probability \n with M = {M}')
    plt.xlabel('s')
    plt.ylabel('$n(s, p)$')
    plt.show()

    #"""


    #"""
    #h

    p_list = np.linspace(0.2, 0.59, 10)
    sl_list = []
    nsl_list = []
    s_xi_list = []
    sl_critical, nsl_critical = estimate_cluster_number_density((L, L), M, p_c)

    fig, ax = plt.subplots(figsize=(8, 5))

    for p in p_list:
        print(p)
        sl, nsl = estimate_cluster_number_density((L, L), M, p)
        sl_list.append(sl)
        nsl_list.append(nsl)
        ax.loglog(sl, nsl, label = f'$p = {p}$')
        if_below = nsl <= 0.5 * nsl_critical[:len(nsl)]

        if not np.any(if_below):
            continue

        index = np.argmax(if_below)
        s_xi = sl[index]
        s_xi_list.append(s_xi)
        ax.scatter(s_xi, nsl[index], label=f'$s_\\xi = {np.round(s_xi, 5)}$')

    plt.legend()
    plt.xlabel('s')
    plt.ylabel('$n(s, p)$')
    plt.title('Estimating $s_\\xi$')
    plt.show()

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(p_list, s_xi_list)
    plt.title('$s_\\xi as a Function of the Percolation Probability$')
    plt.xlabel('$p$')
    plt.xlabel('$s_\\xi$')



    #"""
