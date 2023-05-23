#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from scipy.signal import medfilt

def baseline_correction(ecg_signal):
    return medfilt(ecg_signal, 71)  # Adjust window size as needed

