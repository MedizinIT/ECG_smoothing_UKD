#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import ast
import numpy as np

from baseline_correction import baseline_correction
from smooth_signal import smooth_signal
from apply_lowpass_filter import apply_lowpass_filter
from find_r_peaks import find_r_peaks
from plotting import plot_ecg_with_r_peaks, plot_power_spectral_density
from heart_rate_analysis import calculate_qrs_amplitude, calculate_hrv_measures, calculate_frequency_domain_hrv, calculate_heart_rate

def calculate_qrs_duration(r_peaks, sampling_frequency):
    # Implementation of calculating QRS duration
    qrs_duration = ...  # Calculate the QRS duration using r_peaks and sampling_frequency
    return qrs_duration



def process_ecg_signal(ecg_signal_id, ecg_signal):
    sampling_frequency = 800  # Anpassen ans EKG signal

    # Preprocessing
    baseline_corrected_signal = baseline_correction(ecg_signal)
    smoothed_signal = smooth_signal(baseline_corrected_signal)
    bw_smoothed_signal = apply_lowpass_filter(smoothed_signal)

    # R-peaks detection
    r_peaks, _ = find_r_peaks(bw_smoothed_signal)

    # QRS Duration
    qrs_duration = calculate_qrs_duration(r_peaks, sampling_frequency)

    # Plotting
    plot_ecg_with_r_peaks(ecg_signal, bw_smoothed_signal, r_peaks, ecg_signal_id)
    plot_power_spectral_density(ecg_signal, sampling_frequency)

    # QRS Amplitude
    qrs_amplitude = calculate_qrs_amplitude(bw_smoothed_signal, r_peaks)

    # Heart Rate and HRV
    rr_intervals = np.diff(r_peaks)
    heart_rate = calculate_heart_rate(ecg_signal, r_peaks, sampling_frequency)
    mean_nn, sdnn, rmssd = calculate_hrv_measures(rr_intervals, sampling_frequency)
    lf_power, hf_power, total_power, lfhf_ratio = calculate_frequency_domain_hrv(ecg_signal, sampling_frequency)

    return {
        'ecg_signalid': ecg_signal_id,
        'qrs_duration': qrs_duration,
        'qrs_amplitude': qrs_amplitude,
        'heart_rate': heart_rate,
        'mean_nn': mean_nn,
        'sdnn': sdnn,
        'rmssd': rmssd,
        'lf_power': lf_power,
        'hf_power': hf_power,
        'total_power': total_power,
        'lfhf_ratio': lfhf_ratio,
    }


# Daten auslesen
filename = 'ecg_signal.csv'
df = pd.read_csv(filename)
ecg_signal_ids = df['ecg_signalid'].values
ecg_signals = df['ecg_signal'].apply(lambda x: list(ast.literal_eval(x)['signal'].values())).values

analysis_results = []
for ecg_signal_id, ecg_signal in zip(ecg_signal_ids, ecg_signals):
    result = process_ecg_signal(ecg_signal_id, ecg_signal)
    analysis_results.append(result)

# Analysis results in DataFrame
analysis_df = pd.DataFrame(analysis_results)

# Save analysis results to a new .csv file
analysis_filename = 'ecg_analysis_results.csv'
analysis_df.to_csv(analysis_filename, index=False)

# Abnormal heart rate patterns
abnormal_patterns = []
for i in range(1, len(analysis_results) - 1):
    previous_hr = analysis_results[i - 1]['heart_rate']
    current_hr = analysis_results[i]['heart_rate']
    next_hr = analysis_results[i + 1]['heart_rate']

    if previous_hr > current_hr > next_hr or previous_hr < current_hr < next_hr:
        abnormal_patterns.append(analysis_results[i])

if len(abnormal_patterns) > 0:
    abnormal_df = pd.DataFrame(abnormal_patterns)
    abnormal_filename = 'abnormal_patterns.csv'
    abnormal_df.to_csv(abnormal_filename, index=False)
else:
    print('No abnormal heart rate patterns found.')


# In[ ]:




