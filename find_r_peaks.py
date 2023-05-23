#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy.signal import find_peaks

def find_r_peaks(ecg_signal):
    prominence_threshold = 0.2  # Anpassen
    distance_threshold = 200  # Anpassen
    return find_peaks(ecg_signal, prominence=prominence_threshold, distance=distance_threshold)

