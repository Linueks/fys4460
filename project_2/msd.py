from ovito.io import import_file, export_file
from ovito.modifiers import CalculateDisplacementsModifier
import numpy as np


# Define the custom modifier function:
def modify(frame, data):
    # Access the per-particle displacement magnitudes computed by the
    # CalculateDisplacementsModifier that precedes this user-defined modifier in the
    # data pipeline:
    displacement_magnitudes = data.particles['Displacement Magnitude']

    # Compute MSD:
    msd = np.sum(displacement_magnitudes ** 2) / len(displacement_magnitudes)

    # Output MSD value as a global attribute:
    data.attributes["MSD"] = msd



def wrapper(lammps_dump_file, filename):
    """
    Lacking a better name for the function
    This is just part of an example from the ovito.io docs
    """
    # Load input data and create a data pipeline.
    pipeline = import_file(lammps_dump_file)

    # Calculate per-particle displacements with respect to initial simulation frame:
    pipeline.modifiers.append(CalculateDisplacementsModifier())

    # Insert user-defined modifier function into the data pipeline.
    pipeline.modifiers.append(modify)
    # Export calculated MSD value to a text file and let OVITO's data pipeline do the rest:
    export_file(pipeline, filename,
        format = "txt/attr",
        columns = ["Timestep", "MSD"],
        multiple_frames = True)




if __name__=="__main__":
    filename = "data/msd_data.txt"
    lammps_dump_file = "data/argon_cylinder.lammpstrj"

    wrapper(lammps_dump_file, filename)
