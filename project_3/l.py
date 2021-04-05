import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
from skimage.measure import label, regionprops
from scipy.stats import linregress
plt.style.use('ggplot')

np.random.seed(2021)

def percolation_probability(system_shape, p, num_samples=100):
    n_percolating = 0

    for i in range(num_samples):
        system = np.random.rand(system_shape[0], system_shape[1]) < p
        labels = label(system, connectivity=1)
        props = regionprops(labels)

        for prop in props:
            #check spanning in x and y directions
            span_x = prop.bbox[2] - prop.bbox[0] == system_shape[0]
            span_y = prop.bbox[3] - prop.bbox[1] == system_shape[1]

            if span_x or span_y:
                n_percolating += 1
                break

    return n_percolating / num_samples



def percolation_threshold(system_shape, x, num_samples=100):
    max_iterations = 1000
    tolerance = 1e-6

    lower_bound = 0
    upper_bound = 1

    lower_pi = lower_bound
    upper_pi = upper_bound

    for i in range(max_iterations):
        if upper_bound - lower_bound <= tolerance:
            break

        midpoint = (upper_bound + lower_bound) / 2
        midpoint_pi = percolation_probability(system_shape, midpoint, num_samples)

        if midpoint_pi > x:
            upper_bound = midpoint
            upper_pi = midpoint_pi
        else:
            lower_bound = midpoint
            lower_pi = midpoint_pi

    return midpoint



if __name__=='__main__':
    #numbers from task l) https://www.uio.no/studier/emner/matnat/fys/FYS4460/v20/notes/project2017-ob3.pdf
    L = np.array([5, 10, 15, 25, 50, 100, 150, 200, 400, 800])
    L = L

    x0 = 0.3
    x1 = 0.8
    p_c = 0.59275

    #print(np.random.rand(10, 10) < 0.5)

    threshold0 = []
    threshold1 = []

    for l in L:
        print(l)
        system_shape = (l, l)
        p_pi = percolation_threshold(system_shape, x0)
        threshold0.append(p_pi)

        p_pi = percolation_threshold(system_shape, x1)
        threshold1.append(p_pi)


    threshold0 = np.array(threshold0)
    threshold1 = np.array(threshold1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(L, threshold0, label = f"x = {x0}", marker='o')
    ax.plot(L, threshold1, label = f"x = {x1}", marker='o')
    ax.set_xlabel("system size $L$")
    ax.set_ylabel("$p_{\Pi = x}$")
    ax.set_title("Percolation Threshold as a Function of system size")
    ax.legend()
    plt.show()



    fig2, ax2 = plt.subplots(figsize=(8, 5))
    nu_true = 4/3
    thres_diff = threshold1 - threshold0
    reg = linregress(np.log(L), np.log(thres_diff))

    ax2.plot(np.log(L), np.log(thres_diff), label='Calculated', marker='o')
    ax2.plot(np.log(L), reg.intercept + reg.slope * np.log(L) ,
            label=f'Estimated $\\nu = {np.round(-1/reg.slope, 4)}$',
            linestyle='dashed')
    ax2.plot(np.log(L), reg.intercept - 1/nu_true * np.log(L),
            label=f'True $\\nu = 4/3 = {np.round(nu_true, 4)}$',
            linestyle='dashdot')
    ax2.set_xlabel('$Log(L)$')
    ax2.set_ylabel('$Log(p_{\\Pi} = \Delta x)$')
    ax2.set_title('Scaling of the Percolation Threshold')
    ax2.legend()
    plt.show()


    L_nu = L**(-1/nu_true)
    reg_low = linregress(L_nu, threshold0)
    reg_high = linregress(L_nu, threshold1)

    cx_low = reg_low.slope
    p_c_low = reg_low.intercept
    print(f'Estimated Cx = {cx_low}, p_c = {p_c_low} for x = {x0}')

    cx_high = reg_high.slope
    p_c_high = reg_high.intercept
    print(f'Estimated Cx = {cx_high}, p_c = {p_c_high} for x = {x1}')

    fig, ax3 = plt.subplots(figsize=(8, 5))
    ax3.plot(L_nu, threshold0, marker='o', label='$p_\Pi, x = 0.3$')
    ax3.plot(L_nu, threshold1, marker='o', label='$p_\Pi, x = 0.8$')
    ax3.plot(L_nu, reg_low.intercept + L_nu * reg_low.slope, linestyle='dashed', label='$p_\Pi, x = 0.3$')
    ax3.plot(L_nu, reg_high.intercept + L_nu * reg_high.slope, linestyle='dashed', label='$p_\Pi, x = 0.8$')
    ax3.set_xlabel('$L^{-1/\\nu}$')
    ax3.set_ylabel('$p$')
    ax3.set_title('$L^{-1/\\nu}$ as Function of the Critical \n Percolation Threshold')
    ax3.legend()
    plt.show()


    probs = np.linspace(0.4, 0.7, 21)
    system_sizes = 2**np.arange(4, 10)
    Pi = np.zeros((len(system_sizes), len(probs)))
    # u = (p - p_c)*L_nu
    u = np.zeros_like(Pi)

    for i, l in enumerate(system_sizes):
        print(l)
        u[i] = (probs - p_c) * l**(1 / nu_true)
        for j, p in enumerate(probs):
            Pi[i, j] = percolation_probability((l, l), p)

    fig, ax4 = plt.subplots(figsize=(8, 5))
    for i in range(len(system_sizes)):
        ax4.plot(u[i], Pi[i], label=f'$L = {system_sizes[i]}$')


    ax4.set_xlabel('$(p - p_c)L^{1/\\nu}$')
    ax4.set_ylabel('$\Pi(p, L)$')
    ax4.set_title('Data Collapse Plot for $\\Pi(p, L)$')
    ax4.legend()
    plt.show()
