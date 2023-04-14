import numpy as np
import json
import matplotlib.mlab as mlab
import os
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from ligotools import readligo as rl
from ligotools.utils import *

# data for testing the whiten function:
fn_H1 = 'data/H-H1_LOSC_4_V2-1126259446-32.hdf5'
fn_L1 = 'data/L-L1_LOSC_4_V2-1126259446-32.hdf5'
fnjson = "data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
eventname = 'GW150914'
event = events[eventname]
fs = event['fs']
strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
NFFT = 4*fs
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)
time = time_H1
dt = time[1] - time[0]

# TEST 1
def test_whiten():
	''' 
	Check the length of the output array and if it has a correct type
	'''
	output = whiten(strain_H1,psd_H1,dt)
	assert len(strain_H1) == len(output), "length of the output array does not match the original one"
	assert type(output) == np.ndarray

# Test 2
def test_write_wavfile():
	'''
	Check if the file was written to the correct directory
	'''
	data_arr = np.arange(1, 1000, 0.1)
	write_wavfile('audio/'+eventname, int(fs), data_arr)
	assert os.path.isfile('audio/'+eventname) == True
	
# Test 3
def test_reqshift():
	''' 
	Check the length of the output array and if it has a correct type
	'''
	data_arr = np.arange(1, 1000, 0.1)
	output = reqshift(data_arr, 100, 4096)
	assert type(output) == np.ndarray
	assert len(output) == len(data_arr)

	
# data for testing the plot_results function:
time = np.linspace(-1, 1, 4096)
timemax = 100
SNR = np.abs(np.random.randn(4096))
pcolor = 'g'
det = 'H1'
plottype = 'png'
strain_H1_whitenbp = np.random.randn(4096)
strain_L1_whitenbp = np.random.randn(4096)
template_match = np.random.randn(4096)
tevent = 0.0
template_fft = np.fft.rfft(template_match)
datafreq = np.fft.rfftfreq(len(strain_H1_whitenbp), d=1.0/4096)
d_eff = 1.0
freqs = datafreq
data_psd = np.abs(np.random.randn(len(datafreq)))**2
fs = 4096
strain_whitenbp = np.random.randn(4096)

# Test 4
def test_plot_results():
	'''Check whether the saved file is empty: 
	if the file size is greater than 0, the plot png is saved successfully.
	'''
	plot_results(time, timemax, SNR, pcolor, det, eventname, plottype, tevent, strain_whitenbp, template_match, template_fft, datafreq, d_eff, freqs, data_psd, fs)
	file_path = 'figures/'+eventname+"_"+det+"_SNR."+plottype
	file_size = os.path.getsize(file_path)
	assert file_size > 0
