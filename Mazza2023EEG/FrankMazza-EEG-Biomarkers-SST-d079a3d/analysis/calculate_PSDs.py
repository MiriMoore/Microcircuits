# Import Packages
import numpy as np
from scipy import signal as ss
from sklearn.utils import resample
import LFPy


# Load Dipoles


inputpath = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d/code/Circuit_output_fullsim/Healthy/DIPOLEMOMENT_Seed'
outputpath = '/Users/Miri/Documents/Research/EPhys/Modelling/IQ_Exc/Microcircuits/Mazza2023EEG/FrankMazza-EEG-Biomarkers-SST-d079a3d/data/PV_5.npy'


seedbase = 1

files = np.concatenate([np.arange(1)])
print([str(seedbase+n)+".npy" for n in files])
DIPOLEMOMENTS = [np.load(dp) for dp in [inputpath+str(seedbase+n)+".npy" for n in files]]
print(DIPOLEMOMENTS)

# Variables for analysis, plotting, output
startsclice = 2000          # ms to start timeseries calc
t1 = int(startsclice/0.025) # indicies to start based on startslice

sf = 40000                  # sampling freq
nperseg = int(sf*3)         # 3s window for PSD calc
end_freq = 120              # which frequency to cut (save space)
n_boot = 100                # number of bootstrap iterations


# functions
def getCI(sample,n_boot,alpha):
    
    lower_p = (alpha/2.0) * 100 #95% confidence usually, so 0.05
    upper_p = (1-(alpha/2.0)) * 100
    
    data_t = np.transpose(sample)
    
    bootmeans = []
    
    for row in data_t: #row of data_t is col of data
        rowmean = []
        for i in range(n_boot):
            samples = resample(np.array(row), replace=True, n_samples=round(row.size*.8))
            rowmean.append(samples.mean())
        bootmeans.append(rowmean)
        
    #mean of each row's bootstrapped samples
    means = []
    for row in bootmeans:
        means.append(np.array(row).mean())

    #get CI for each row
    CIs_upper = []
    CIs_lower = []
    for row in bootmeans:
        CIs_upper.append(np.percentile(row,upper_p))
        CIs_lower.append(np.percentile(row,lower_p))
    
    return means,CIs_lower,CIs_upper



# Collect EEG timeseries, save into dict
print('Calculating EEG timeseries from summed population dipolemoments ...')

# create empty dicts to hold data
EEG = {}

# params for forward solution
radii = [79000., 80000., 85000., 90000.] # radii of four sphere
sigmas = [0.47, 1.71, 0.02, 0.41]        # conductivity for each sphere
rz = np.array([0., 0., 78250.])          # dipole location
r2 = np.array([[0., 0., 90000]])         # sensor location

# print(DIPOLEMOMENTS[0].keys())

# EEG_args = LFPy.FourSphereVolumeConductor(radii, sigmas, r2)
EEG_args = LFPy.FourSphereVolumeConductor(r_electrodes=r2, radii=radii, sigmas=sigmas)

for j, run in enumerate(DIPOLEMOMENTS):
    
    dp = np.add(np.add(run['HL23PN1'],run['HL23MN1']),
                np.add(run['HL23BN1'],run['HL23VN1']))
    
    EEG_temp = EEG_args.calc_potential(dp, rz)

    key = str(seedbase+j)
    d = {str(key):{'ts_raw':EEG_temp.flatten()}}
    EEG.update(d)
    

# Calc PSDs
print('>>> Calculating EEG PSDs ...')
for seedname,seed in EEG.items():
    for ts_name,timeseries in seed.items():
        w = {}
        ts = timeseries.flatten()[t1:] # cut transient
        freq_wel, ps_wel = ss.welch(ts,fs=sf,nperseg=nperseg)
        
        end_wel = int(end_freq/freq_wel[1])
        
        w = {'ps_wel':ps_wel[:end_wel]}
        
    seed.update(w)
    
    
# Bootstrap data
print('>>> Bootstrapping EEGs ...')

psds_wel = []

for seedname,seed in EEG.items():
    for dataname,data in seed.items():
        if dataname == 'ps_wel':
            psds_wel.append(data)

psds_wel = np.array(psds_wel) 

bootmean,upper,lower = getCI(psds_wel,n_boot,0.05)

EEG.update({'mean_psd':{'ps_wel':psds_wel.mean(axis=0),
                        'sd_wel':psds_wel.std(axis=0),
                        'freq_wel':freq_wel[:end_wel],
                        'ps_wel_bm':bootmean,
                        'ps_wel_upper':upper,
                        'ps_wel_lower':lower}})


print('>>> Saving EEGs')
np.save(outputpath,EEG)
