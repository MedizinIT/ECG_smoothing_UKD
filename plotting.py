#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt

from scipy.signal import welch


def plot_ecg_with_r_peaks(ecg_signal, bw_smoothed_signal, r_peaks, ecg_signal_id):
    plt.figure(figsize=(10, 6))
    plt.plot(ecg_signal, label='Original Signal')
    plt.plot(bw_smoothed_signal, label='Filtered Signal')
    plt.plot(r_peaks, bw_smoothed_signal[r_peaks], 'ro', label='R-Peaks')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.title(f'ECG Signal {ecg_signal_id} with R-Peaks')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_power_spectral_density(ecg_signal, sampling_frequency):
    f, psd = welch(ecg_signal, fs=sampling_frequency)
    plt.figure(figsize=(8, 6))
    plt.plot(f, psd)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density')
    plt.title('Power Spectral Density of ECG Signal')
    plt.grid(True)
    plt.show()

