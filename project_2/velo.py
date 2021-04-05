import numpy as np
import matplotlib.pyplot as plt


plt.style.use('ggplot')


def plotter(filename):
    with open(filename) as infile:

        infile.readline()

        lines = infile.readlines()

        velocities = np.zeros(len(lines))
        position_y = np.zeros(len(lines))

        i = 0
        for line in lines:
            words = line.split('\t')
            #print(i)
            velocities[i] = words[0]
            position_y[i] = words[1]
            i += 1



        mask = np.where(velocities != 0)
        velocities = velocities[mask]
        position_y = position_y[mask]
        polyfit = np.poly1d(np.polyfit(position_y, velocities, 2))

        coeffs = np.polyfit(position_y, velocities, 2)


        #polyfit = np.poly1d(np.polyfit(velocities, position_y, 2))
        x = np.linspace(np.sort(position_y)[0], np.sort(position_y)[-1], 1000)

        #plt.scatter(np.sort(position_y), velocities)
        #plt.show()
        ax1 = plt.subplot(2,1,1)
        ax1.set_title("Flow Velocity Distribution")
        ax1.set_xlabel("$v_x$")
        ax1.set_ylabel("y-position")
        plt.scatter(velocities, position_y)
        ax2 = plt.subplot(2,1,2, sharex=ax1)
        plt.plot(x**2 * coeffs[0] + x * coeffs[1] + coeffs[0], x)
        #ax2.set_xticks([])
        #plt.plot(polyfit[0] + polyfit[1]*x + polyfit[2]*x**2)
        #plt.plot(polyfit(position_y[velo_mask]))
        plt.show()


if __name__=='__main__':
    file = "data/velocity_profile.txt"
    plotter(file)
