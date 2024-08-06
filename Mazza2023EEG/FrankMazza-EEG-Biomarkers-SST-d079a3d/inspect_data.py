import numpy as np
import pandas as pd
import h5py
import pickle
import os


#%%
# Define the file path
file_path = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d/code/Circuit_output_fullsim/Healthy/DIPOLEMOMENT_Seed1.npy'

# Load the .npy file
dipole_moments = np.load(file_path, allow_pickle=True)

# Check the type and dimensions of the loaded object
if isinstance(dipole_moments, np.ndarray):
    # Print the shape of the loaded ndarray
    print(f"Shape of the loaded ndarray: {dipole_moments.shape}")

    # Check if the array is 0-dimensional
    if dipole_moments.ndim == 0:
        print("Loaded ndarray is 0-dimensional.")
        print("Content of the loaded ndarray:")
        print(dipole_moments)
    else:
        # Print the first few elements of the ndarray
        print("First few elements of the loaded ndarray:")
        print(dipole_moments[:5])
else:
    # Print the type and content of the loaded object
    print(f"Loaded object is of type: {type(dipole_moments)}")
    print("Content of the loaded object:")
    print(dipole_moments)

#%%
# Define the file path
file_path = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d/code/Circuit_output_testing/cell_positions_and_rotations.h5'

# Open the HDF5 file and inspect its contents
try:
    with h5py.File(file_path, 'r') as h5file:
        # List all datasets in the file
        print("Datasets in the file:")
        for name in h5file:
            print(name)

        # Read and print the content of each dataset
        for name in h5file:
            data = pd.read_hdf(file_path, key=name)
            print(f"\nContent of dataset '{name}':")
            print(data)
except Exception as e:
    print(f"An error occurred: {e}")

#%%
# Define the file path
file_path = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d/code/Circuit_output_testing/SPIKES_Seed1.pkl'

# Load the .pkl file
with open(file_path, 'rb') as f:
    spikes_data = pickle.load(f)

# Inspect the contents of the loaded data
print(f"Type of loaded data: {type(spikes_data)}")

# Print a summary of the contents
if isinstance(spikes_data, dict):
    print("Keys in the dictionary:")
    for key in spikes_data.keys():
        print(f"  {key}: {type(spikes_data[key])}, length: {len(spikes_data[key])}")
else:
    print("Content of the loaded data:")
    print(spikes_data)