#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from scipy.signal import welch

def calculate_qrs_amplitude(bw_smoothed_signal, r_peaks):
    return np.max(bw_smoothed_signal[r_peaks]) - np.min(bw_smoothed_signal[r_peaks])

def calculate_hrv_measures(rr_intervals, sampling_frequency):
    nn_intervals = rr_intervals / sampling_frequency
    mean_nn = np.mean(nn_intervals)
    sdnn = np.std(nn_intervals)
    rmssd = np.sqrt(np.mean(np.square(np.diff(nn_intervals))))
    return mean_nn, sdnn, rmssd

def calculate_frequency_domain_hrv(ecg_signal, sampling_frequency):
    f, psd = welch(ecg_signal, fs=sampling_frequency)

    lf_band = (0.04, 0.15)  # Low-frequency band (anpassen)
    hf_band = (0.15, 0.4)  # High-frequency band (anpassen)

    lf_power = np.trapz(psd[(f >= lf_band[0]) & (f <= lf_band[1])], f[(f >= lf_band[0]) & (f <= lf_band[1])])
    hf_power = np.trapz(psd[(f >= hf_band[0]) & (f <= hf_band[1])], f[(f >= hf_band[0]) & (f <= hf_band[1])])
    total_power = np.trapz(psd, f)

    # Calculate LF/HF ratio (handle division by zero)
    if hf_power != 0:
        lfhf_ratio = lf_power / hf_power
    else:
        lfhf_ratio = np.nan

    return lf_power, hf_power, total_power, lfhf_ratio

def calculate_heart_rate(ecg_signal, r_peaks, sampling_frequency):
    duration_in_minutes = len(ecg_signal) / (sampling_frequency * 60)  # Adjust the sampling frequency if necessary
    heart_rate = len(r_peaks) / duration_in_minutes
    return heart_rate

