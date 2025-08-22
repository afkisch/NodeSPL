import math

def invert(param_dict:dict):
    return -1*param_dict['scale']

# ========= NORMALIZATION ==========
# Min-max scaling
# Usecase: sensors with absolute range
def min_max_scale(signal, new_min=0.0, new_max=1.0):
    
    old_min = min(signal)
    old_max = max(signal)
    
    if old_max-old_min == 0:
        return signal # Avoid div by zero
    
    return [((x-old_min)/(old_max-old_min))*(new_max-new_min)+new_min for x in signal]


# Z-score
# Usecase: ECG, vibration (absolute scale is not important)
def zscore(signal):
    
    mean_val = sum(signal) / len(signal)
    std_val = math.sqrt(sum((x-mean_val)**2 for x in signal) / len(signal))
    
    if std_val == 0:
        return signal

    return [(x-mean_val) / std_val for x in signal]


# Decimal scaling (log10)
# Usecase: large varying magnitudes
def decimal_scale(signal):
    
    max_abs_val = max(abs(x) for x in signal)
    if max_abs_val == 0:
        return signal
    
    j = math.ceil(math.log10(max_abs_val+1))
    return [x / (10**j) for x in signal]


# Max abs scale (-1...1)
# Usecase: motor control, acceleration sensor
def max_abs_scale(signal):
    max_abs_val = max(abs(x) for x in signal)
    if max_abs_val == 0:
        return signal
    return [x / max_abs_val for x in signal]


# Baseline norm
# Usecase: DC removal
def baseline_norm(signal):
    mean_val = sum(signal) / len(signal)
    return [x-mean_val for x in signal]

# ==================================

# =========== FILTERING ============

def moving_average(signal, window_size):
    if len(signal) < window_size:
        return []
    result = []
    total = sum(signal[:window_size])
    result.append(total / window_size)
    for i in range(window_size, len(signal)):
        total += signal[i] - signal[i - window_size]
        result.append(total / window_size)
    return result

def low_pass(signal, alpha):
    if not signal:
        return []
    result = [signal[0]]
    for i in range(1, len(signal)):
        result.append(alpha * signal[i] + (1 - alpha) * result[-1])
    return result

def high_pass(signal, alpha):
    if not signal:
        return []
    result = [0]
    for i in range(1, len(signal)):
        y = alpha * (result[-1] + signal[i] - signal[i-1])
        result.append(y)
    return result

# ==================================


PROCESSING_FUNCTIONS = {
    "min_max_scale" : min_max_scale,
    "zscore" : zscore,
    "decimal_scale" : decimal_scale,
    "max_abs_scale" : max_abs_scale,
    "baseline" : baseline_norm,

    "moving_average" : moving_average,
    "low_pass" : low_pass,
    "high_pass" : high_pass
}