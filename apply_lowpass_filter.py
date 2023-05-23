#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy.signal import butter, filtfilt

def apply_lowpass_filter(ecg_signal):
    cutoff_frequency = 0.01  # Anpassen für smoothing
    butter_order = 2
    nyquist_frequency = 0.5
    normalized_cutoff = cutoff_frequency / nyquist_frequency
    b, a = butter(butter_order, normalized_cutoff, btype='low')
    return filtfilt(b, a, ecg_signal)

