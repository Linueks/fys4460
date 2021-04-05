import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as spi
import skimage as ski
from skimage.measure import label, regionprops

plt.style.use('ggplot')


def cumulative_distribution(sample):
    sum = np.cumsum(sample)
    norm = np.max(sum)

    return sum / norm



def log_bin(data, n_bins=10):
    log_max = np.ceil(np.max(np.log(data) / np.log(10)))

    bins = np.logspace(0, log_max, n_bins, base=10)
    widths = bins[1:] - bins[:-1]

    hist = np.histogram(data, bins=bins)
    norm = hist[0] / widths

    return norm, bins, widths



if __name__=='__main__':
    """
    In this task we are to determine the distribution function for a set of
    random numbers raised to -2..
    """

    sample = np.sort(np.random.rand(int(1e6)) ** (-3+1))                        #-2 is written like this in the task for some weird reason...

    fig, ax = plt.subplots(figsize=(16, 10))

    cdf = cumulative_distribution(sample)

    ax.loglog(sample, cdf)
    plt.title('Plot of $P(Z>z)$')
    plt.xlabel('x')
    plt.ylabel('$P(Z>z)$')
    plt.show()


    fig, ax = plt.subplots(figsize=(16, 10))
    f_z = np.gradient(cdf)
    ax.loglog(sample, f_z)
    plt.title('Distribution function $f_z$')
    plt.xlabel('z')
    plt.ylabel('$f_z$')
    plt.show()


    fig, ax = plt.subplots(figsize=(16, 10))
    hist, bins, widths = log_bin(sample)
    ax.bar(bins[1:], hist, widths)
    ax.set(xticks=bins[1:])
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Logarithmic Binning of Distribution function $f_z$')
    plt.show()
