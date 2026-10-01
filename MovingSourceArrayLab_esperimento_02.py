# 02) STATIC POINT SOURCE --> SIGNALS AT THE MICROPHONES

import numpy as np
import matplotlib.pyplot as plt

# FIXED PARAMETERS
c = 343.0 # sound velocity [m/s]
fs = 48000 # sampling frequency [Hz]
duration = 0.01 # signal duration [s]
f0 = 2000.0 # source frequency [Hz]

# MICROPHONE ARRAY
M = 8 # number of microphones
d = 0.05 # distance between microphones

mic_x = (np.arange(M) - (M-1)/2) * d # position of microphones centered in zero
mic_y = np.zeros(M)

# SOURCE POSITION
source_x = 0.30 # meters
source_y = 1.00 # meters

# SOURCE-MICROPHONE DISTANCE
distance = np.sqrt((source_x - mic_x)**2 + (source_y - mic_y)**2)

# absolute propagation times
arrival_times = distance/c

# relative delay with respect to the first-arriving microphone
relative_delays = arrival_times - np.min(arrival_times)

# TIME AXIS
N = int(fs*duration)
t = np.arange(N)/fs

# SOURCE SIGNAL
source_signal = np.sin(2 * np.pi * f0 * t)

# SIGNAL RECEIVED BY EACH MICROPHONE
mic_signals = np.zeros((M, N))

for m in range(M):
    tau = relative_delays[m]
    mic_signals[m, :] = np.sin(2 * np.pi * f0 * (t - tau))


# PRINT SOME INFORMATION
print()
print("Relative delays [ms]:")
print(relative_delays * 1e6)

print()
print("Relative delays [samples]:")
print(relative_delays * fs)

# PLOR FIRST THREE MICROPHONES
plt.figure(figsize=(10,7))

plt.plot(t*1000, mic_signals[0], label="Mic 0")
plt.plot(t*1000, mic_signals[3], label="Mic 3")
plt.plot(t*1000, mic_signals[7], label="Mic 7")

plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")

plt.title(
    "MovingSourceArrayLab - Experiment 02\n"
    "Signals received by different microphones"
)

plt.grid()
plt.legend()

plt.show()