import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile as llf
from scipy.stats import linregress

plt.style.use('ggplot')





file = f'data/low_density.log'

log = llf.File(file)
time = log.get('v_time')
pressure = log.get('Press')
temperature = log.get('c_pore_temp')
msd = log.get('c_msd[4]')





#lineplot = ax.plot(time, kinetic_energy, label=f'$<E_k>$')
#lineplot = ax.plot(time, pressure, label='Logged Pressure')
#lineplot = ax.plot(time, 4000 * temperature / 400000, label='Ideal Gas Law')


fig, ax1 = plt.subplots(figsize=(16,8))

res = linregress(time, msd)


msd_plot = ax1.plot(time, msd,
                label='Mean Square Displacement')
reg_plot = ax1.plot(time, res.intercept + res.slope * time,
                label=f'Linear Regression a={round(res.slope, 3)}')
ax1.set_ylabel('$<r^2(t)>$')
ax1.set_xlabel('Time [LJ units]')
plt.legend()
plt.show()



fig, ax2 = plt.subplots(figsize=(16,8))

pressure_plot = ax2.plot(time, pressure) #lol


ax2.set_ylabel('Pressure [LJ units]')
ax2.set_xlabel('Time [LJ units]')
ax2.set_title(f'Pressure for Low Density Porous System')
plt.legend()
plt.show()


fig, ax3 = plt.subplots(figsize=(16,8))

temperature_plot = ax3.plot(time, temperature) #lol


ax3.set_ylabel('Pore Temperature [LJ units]')
ax3.set_xlabel('Time [LJ units]')
ax3.set_title(f'Pore Temperature for Low Density Porous System')
plt.legend()
plt.show()
