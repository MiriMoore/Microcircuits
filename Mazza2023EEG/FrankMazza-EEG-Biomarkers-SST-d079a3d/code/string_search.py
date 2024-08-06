import os
import fnmatch
#%%
def search_string_in_files(directory_path, search_string, file_pattern='*'):
    for root, dirs, files in os.walk(directory_path):
        for file_name in fnmatch.filter(files, file_pattern):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_number, line in enumerate(file, start=1):
                    if search_string in line:
                        print(f'Found "{search_string}" in {file_path} on line {line_number}')

# Define the directory path and the string to search for
directory_path = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d'
search_string = 'tonic'

# Call the function
search_string_in_files(directory_path, search_string)