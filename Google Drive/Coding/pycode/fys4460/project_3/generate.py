import numpy as np
import matplotlib.pyplot as plt




L = 10
p = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

for p in p:
    r = np.random.rand(L, L)
    z = r<p
    plt.imshow(z, cmap='Greys', origin='lower')
    plt.title(f'Random System p = {p}')
    plt.show()
