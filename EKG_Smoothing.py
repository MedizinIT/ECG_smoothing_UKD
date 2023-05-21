#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, butter, filtfilt, medfilt, find_peaks

filename = 'ecg_signal.csv'
df = pd.read_csv(filename)

# Daten extrahieren
ecg_signal_ids = df['ecg_signalid'].values
ecg_signals = df['ecg_signal'].apply(lambda x: list(ast.literal_eval(x)['signal'].values())).values

smoothed_signals = []

for ecg_signal_id, ecg_signal in zip(ecg_signal_ids, ecg_signals):
    # Smoothing mit Savitzky-Golay Filter
    window_size = 70  # Anpassen Smoothing
    polynomial_order = 3
    sg_smoothed_signal = savgol_filter(ecg_signal, window_size, polynomial_order)

    # Danach Butterworth filter
    cutoff_frequency = 0.01  # Anpassen Smoothing
    butter_order = 2
    nyquist_frequency = 0.5
    normalized_cutoff = cutoff_frequency / nyquist_frequency
    b, a = butter(butter_order, normalized_cutoff, btype='low')
    bw_smoothed_signal = filtfilt(b, a, sg_smoothed_signal)

    # Und als letztes Median Filter
    median_window_size = 3  # Anpassen Smoothing
    median_smoothed_signal = medfilt(bw_smoothed_signal, median_window_size)

    smoothed_signals.append(median_smoothed_signal)

    # peaks Suchen im smoothed EKG
    peaks, _ = find_peaks(median_smoothed_signal, distance=200)

    # Plotting with peaks
    plt.figure()
    plt.plot(ecg_signal, label='Original Signal')
    plt.plot(median_smoothed_signal, label='Smoothed Signal')
    plt.title(f'ECG Signal {ecg_signal_id}')
    plt.plot(peaks, median_smoothed_signal[peaks], 'ro', label='Peaks')
    plt.title(f'ECG Signal {ecg_signal_id} with Peaks')
    plt.legend()
    plt.show()

    # QRS-KOmplex-Amplitude berechnen
    qrs_amplitude = np.max(median_smoothed_signal[peaks]) - np.min(median_smoothed_signal[peaks])

    print(f"ECG Signal ID {ecg_signal_id}:")
    print(f"QRS Amplitude: {qrs_amplitude}")
    print("")

# smoothed signals in Data Frame speichern
smoothed_data = {'ecg_signalid': [], 'smoothed_signal': []}

# Für jedes EKG
for ecg_signal_id, smoothed_signal in zip(ecg_signal_ids, smoothed_signals):
    smoothed_data['ecg_signalid'].extend([ecg_signal_id] * len(smoothed_signal))
    smoothed_data['smoothed_signal'].extend(smoothed_signal)

smoothed_df = pd.DataFrame(smoothed_data)

# Data frame in neues .csv speichern
smoothed_filename = 'smoothed_ecg_signal.csv'
smoothed_df.to_csv(smoothed_filename, index=False)


# In[ ]:




