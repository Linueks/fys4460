import pandas as pd
import numpy as np
import re


"""
ugliest shit ive ever written, dont judge me
"""


file_path = "task_f/dump.lammpstrj"


def lammps_to_csv(file):
    """
    lammps dumpfiles have the header:

    ITEM: TIMESTEP                                          line 0
    0                                                       line 1
    ITEM: NUMBER OF ATOMS                                     .
    4000                                                      .
    ITEM: BOX BOUNDS pp pp pp                                 .
    0.0000000000000000e+00 7.3680629972807722e+01             .
    0.0000000000000000e+00 7.3680629972807722e+01             .
    0.0000000000000000e+00 7.3680629972807722e+01             .
    ITEM: ATOMS id type x y z vx vy vz                      line 8
    """

    column_names = ['atom_index, atom_type, x, y, z, vx, vy, vz']

    index = []
    pos_x = []
    pos_y = []
    pos_z = []

    with open(file) as infile:
        lines = infile.readlines()
        original_length = len(lines)

        for i, line in enumerate(lines):
            if i % 4009 <= 8:
                continue

            words = line.split(' ')
            index.append(int(words[0]))
            pos_x.append(float(words[2]))
            pos_y.append(float(words[3]))
            pos_z.append(float(words[4]))


        index = np.asarray(index)
        pos_x = np.asarray(pos_x)
        pos_y = np.asarray(pos_y)
        pos_z = np.asarray(pos_z)

        return index, pos_x, pos_y, pos_z, original_length



def mean_square_displacement(index, x, y, z):


    atoms = np.arange(0, 4000)

    atoms = np.zeros((4000, 3, len(x)))


    for i in range(len(index)):
        position = []
        position.append(x[i])
        position.append(y[i])
        position.append(z[i])
        current_atom = index[i] - 1
        atoms[current_atom] = np.asarray(position)

        #atoms[atom_index] = np.array(position)

    print(atoms[0, :])

    return




atom_index, x, y, z, orig_len = lammps_to_csv(file_path)
print(orig_len)
print(atom_index.shape, x, y.shape, z.shape)

mean_square_displacement(atom_index, x, y, z)
