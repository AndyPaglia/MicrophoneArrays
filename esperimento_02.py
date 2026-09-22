# 2) 1 SINUSOIDAL SOURCE + 2 MICROPHONES --> DELAY OBSERVATIONS

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI
c = 343 # m/s

mic1 = np.array([-0.1, 0.0])
mic2 = np.array([ 0.1, 0.0])

source = np.array([0.6, 1.0])

# DISTANZE

r1 = np.linalg.norm(source - mic1)
r2 = np.linalg.norm(source - mic2)

# TEMPI DI ARRIVO

t1 = r1 / c
t2 = r2 / c

tdoa = t1 - t2

print("r1 =", r1, "m")
print("r2 =", r2, "m")

print("t1 =", t1 * 1000, "ms")
print("t2 =", t2 * 1000, "ms")

print("TDOA =", tdoa * 1e6, "microsecondi")

# PARAMETRI SEGNALE

fs = 48000       # sampling rate [Hz]
f0 = 3000        # frequenza sorgente [Hz]
duration = 0.01  # 10 ms

t = np.arange(0, duration, 1/fs)

# SEGNALE ALLA SORGENTE

source_signal = np.sin(2 * np.pi * f0 * t)

# SEGNALI AI MICROFONI

signal_mic1 = np.zeros_like(t)
signal_mic2 = np.zeros_like(t)

mask1 = t >= t1
mask2 = t >= t2

signal_mic1[mask1] = (1 / r1) * np.sin(2 * np.pi * f0 * (t[mask1] - t1))

signal_mic2[mask2] = (1 / r2) * np.sin(2 * np.pi * f0 * (t[mask2] - t2))

# RITARDO IN CAMPIONI

delay_samples = tdoa * fs

print("TDOA in campioni =", delay_samples)

# GRAFICO

plt.figure(figsize=(10, 5))

plt.plot(
    t * 1000,
    signal_mic1,
    label="Mic 1"
)

plt.plot(
    t * 1000,
    signal_mic2,
    label="Mic 2",
    alpha=0.8
)

plt.xlabel("Tempo [ms]")
plt.ylabel("Ampiezza")

plt.title("Segnali ricevuti dai due microfoni")

plt.grid()
plt.legend()

plt.xlim(2.5, 5)

plt.show()