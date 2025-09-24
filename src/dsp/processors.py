import numpy as np
from scipy.signal import butter, filtfilt, medfilt, find_peaks, decimate

# -------------------------------
# Utility
# -------------------------------


def passthrough(signal, **kwargs):
    """Return the signal unchanged"""
    return signal


def scale(signal, factor=1.0, offset=0.0, **kwargs):
    """Scale signal linearly: y = factor*x + offset"""
    return (np.array(signal) * factor + offset).tolist()


def normalize_minmax(signal, **kwargs):
    """Normalize signal to [0, 1]"""
    sig = np.array(signal)
    if sig.size == 0:
        return signal
    return ((sig - sig.min()) / (sig.max() - sig.min())).tolist()

def remove_baseline_median(signal, fs=250, win_sec=0.6):
    """
    Remove ECG baseline wander using median filtering.

    Parameters
    ----------
    signal : array_like
        Input ECG signal.
    fs : int, optional
        Sampling frequency in Hz (default: 250 Hz).
    win_sec : float, optional
        Median filter window length in seconds (default: 0.6 s).
        Should be longer than QRS duration (~0.12 s).

    Returns
    -------
    filtered : ndarray
        Baseline-corrected ECG signal.
    """
    sig = np.asarray(signal, dtype=float)
    win = int(win_sec * fs)
    if win % 2 == 0:  # median filter window must be odd
        win += 1
    baseline = medfilt(sig, kernel_size=win)
    return sig - baseline

# -------------------------------
# Basic DSP
# -------------------------------


def bandpass(signal, low=0.5, high=40, fs=250, order=4, **kwargs):
    """Apply bandpass filter"""
    if len(signal) < 15:  # avoid filtfilt error on short signals
        return signal
    nyq = 0.5 * float(fs)
    b, a = butter(order, [float(low) / nyq, float(high) / nyq], btype="band")
    return filtfilt(b, a, signal).tolist()


def lowpass(signal, cutoff=40, fs=250, order=4, **kwargs):
    """Apply lowpass filter"""
    if len(signal) < 15:
        return signal
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype="low")
    return filtfilt(b, a, signal).tolist()


def highpass(signal, cutoff=0.5, fs=250, order=4, **kwargs):
    """Apply highpass filter"""
    if len(signal) < 15:
        return signal
    nyq = 0.5 * fs
    b, a = butter(order, cutoff / nyq, btype="high")
    return filtfilt(b, a, signal).tolist()


def moving_average(signal, window=5, **kwargs):
    """Smooth signal with moving average"""
    sig = np.array(signal)
    if len(sig) < window:
        return signal
    return np.convolve(sig, np.ones(window) / window, mode="valid").tolist()


def median_filter(signal, kernel=3, **kwargs):
    """Remove spikes using median filter"""
    return medfilt(signal, kernel_size=kernel).tolist()


def downsample_signal(signal, factor=5, **kwargs):
    return decimate(signal, factor, zero_phase=False).tolist()

# -------------------------------
# Feature Extraction
# -------------------------------


def mean(signal, **kwargs):
    return float(np.mean(signal)) if len(signal) > 0 else None


def variance(signal, **kwargs):
    return float(np.var(signal)) if len(signal) > 0 else None


def signal_energy(signal, **kwargs):
    return float(np.sum(np.array(signal) ** 2))


def zscore(signal, **kwargs):
    arr = np.array(signal)
    return ((arr - np.mean(arr)) / (np.std(arr) + 1e-8)).tolist()


def fft_spectrum(signal, fs=250, **kwargs):
    """Compute FFT spectrum magnitude"""
    sig = np.array(signal)
    freqs = np.fft.rfftfreq(len(sig), 1 / fs)
    spectrum = np.abs(np.fft.rfft(sig))
    return {"freqs": freqs.tolist(), "spectrum": spectrum.tolist()}

# -------------------------------
# Anomaly Detection
# -------------------------------


def zscore_threshold(signal, limit=3.0, **kwargs):
    """Return True if signal has outlier above z-score limit"""
    sig = np.array(signal)
    if sig.size == 0:
        return False
    zscores = (sig - sig.mean()) / sig.std()
    return bool(np.any(np.abs(zscores) > limit))


def threshold_anomaly(signal, low=-3, high=3, **kwargs):
    anomalies = [abs(x) > high or x < low for x in signal]
    return any(anomalies)

# -------------------------------
# ECG-specific
# -------------------------------


def r_peak_detection(signal, fs=250, height=None, distance=None, **kwargs):
    """Detect R-peaks using scipy.find_peaks"""
    sig = np.array(signal)
    distance = distance or int(0.35 * fs)  # ~250ms refractory period
    threshold = height or 0.6 * np.max(sig)
    peaks, _ = find_peaks(sig, height=threshold, distance=distance)
    return peaks.tolist()


def hr_calc(signal, fs=250, **kwargs):
    """Estimate HR from R-peak indices"""
    signal = np.array(signal)
    if len(signal) < 2:
        return None
    rr_intervals = np.diff(signal) / fs  # seconds
    mean_rr = np.mean(rr_intervals)
    print('mean_ hr--------------------------', mean_rr)
    hr = 60.0 / mean_rr
    return float(hr)


PROCESSING_FUNCTIONS = {
    'passthrough': passthrough,
    'scale': scale,
    'normalize': normalize_minmax,
    'bandpass': bandpass,
    'lowpass': lowpass,
    'highpass': highpass,
    'moving_average': moving_average,
    'median_filter': median_filter,
    'mean': mean,
    'variance': variance,
    'signal_energy': signal_energy,
    'zscore': zscore,
    'zscore_threshold': zscore_threshold,
    'threshold_anomaly': threshold_anomaly,
    'r_peak': r_peak_detection,
    'hr_calc': hr_calc,
    'downsample': downsample_signal,
    'baseline_median': remove_baseline_median
}
