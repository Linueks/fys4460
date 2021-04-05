import pylab as pylab
import matplotlib.pyplot as plt
from scipy.ndimage import measurements


pylab.seed(2021)

L = 10
r = pylab.rand(L, L)
#p = pylab.arange(0.2, 0.7, 0.1)
p = 0.6
z = r<p




lw, num = measurements.label(z)
b = pylab.arange(lw.max() + 1)
pylab.shuffle(b)
shuffled_lw = b[lw]


area = measurements.sum(z, lw, index = pylab.arange(lw.max() + 1))
area_image = area[lw]



f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.imshow(z, cmap='Greys', origin='lower')
ax1.set_title('z')

ax2.imshow(lw, cmap='Greys', origin='lower')
ax2.set_title('lw')

ax3.imshow(shuffled_lw, cmap='jet', origin='lower')
ax3.set_title('shuffled lw')

ax4.imshow(area_image, cmap='jet', origin='lower')
ax4.set_title('area image')

plt.tight_layout()
plt.show()
