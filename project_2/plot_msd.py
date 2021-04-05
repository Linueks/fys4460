import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
plt.style.use('ggplot')




def plotter(filename):
    with open(filename) as infile:

        infile.readline()

        lines = infile.readlines()

        displacements = np.zeros(len(lines))
        timesteps = np.zeros(len(lines))

        i = 0
        for line in lines:
            words = line.split(' ')
            displacements[i] = words[1]
            timesteps[i] = words[0]
            i += 1

        res = linregress(timesteps, displacements * 30907/1093 * 10 * len(timesteps))


        print(len(timesteps))
        plt.plot(timesteps, displacements * 30907/1093 * 10 * len(timesteps),
                    label="$<r^2(t)>$")
        plt.plot(timesteps, res.intercept + res.slope*timesteps,
                    label=f"Linear Regression with $a$={res.slope}",
                    linestyle='dashed')

        plt.xlabel('Simulation Time')
        plt.ylabel('Mean Squared Displacement')
        plt.title('Mean Squared Displacement for Argon system')
        plt.legend()
        plt.show()


if __name__=="__main__":
    filename = "data/msd_data.txt"
    plotter(filename)
