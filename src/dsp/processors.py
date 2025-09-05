import numpy as np
from scipy.signal import butter, filtfilt

def passthrough(signal, **kwargs):
    """Return input data unchanged."""
    return signal

def zscore(signal, **kwargs):
    arr = np.array(signal)
    return ((arr - np.mean(arr)) / (np.std(arr) + 1e-8)).tolist()

def bandpass(signal, low=0.5, high=40, fs=250, order=4, **kwargs):
    if len(signal) >= 3*order:
        nyq = 0.5*fs
        b, a = butter(order, [low/nyq, high/nyq], btype='band')
        return filtfilt(b, a, signal).tolist()
    else:
        return signal

def threshold_anomaly(signal, low=-3, high=3, **kwargs):
    anomalies = [abs(x)>high or x<low for x in signal]
    return any(anomalies)


PROCESSING_FUNCTIONS = {
    'passthrough': passthrough,
    'zscore': zscore,
    'bandpass': bandpass,
    'threshold': threshold_anomaly,
}