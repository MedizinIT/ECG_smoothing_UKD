#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy.signal import savgol_filter

def smooth_signal(ecg_signal):
    window_size = 71  # Anpassen für smoothing
    polynomial_order = 3
    return savgol_filter(ecg_signal, window_size, polynomial_order)

