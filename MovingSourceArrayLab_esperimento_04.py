# 04) POINT SPREAD FUNCTION

# Capire perchè una sorgente puntiforme non appare come un punto nella beam map
# Mettiamo sorgente al centro e osserviamo la risposta dell'array

import numpy as np
import matplotlib.pyplot as plt

# FIXED PARAMETERES
c = 343.0
f0 = 2000.0
fs = 48000
duration = 0.02

# MICROPHONE ARRAY
M = 8
d = 0.05

mic_x = (np.arange(M) - (M - 1)/2) * duration
mic_y = np.zeros(M)

# POINT SOURCE
source_x = 0.30
source_y = 1.0

# TIME AXIS
N = int(duration*fs)
t = np.arange(N)/fs

# TRUE SOURCE --> MICROPHONE DELAYS
distances = np.sqrt((source_x - mic_x)**2 + (source_y - mic_y)**2)
arrival_times = distances/c
relative_delays = arrival_times - np.min(arrival_times)

# MICROPHONE SIGNALS
mic_signals = np.zeros((M, N))

for m in range(M):
    tau = relative_delays[m]
    mic_signals[m] = np.sin(2 * np.pi * f0 * (t - tau))

# SCANNING GRID
x_scan = np.linspace(-1.0, 1.0, 101)
y_scan = np.linspace(0.2, 2.0, 101)

beam_map = np.zeros((len(x_scan), len(y_scan)))

# DELAY AND SUM BEAMFORMING
for iy, y in enumerate(y_scan):
    for ix, x in enumerate(x_scan):
        # expected distances if source were at (x, y)
        scan_distances = np.sqrt((x - mic_x)**2+ (y - mic_y)**2)

        # expected propagation times
        scan_times = scan_distances/c

        # expected relative delays
        scan_delays = (scan_times - np.min(scan_times))

        # Convert delays to samples
        delay_samples = np.round(scan_delays*fs).astype(int)

        # Align microphone signals
        aligned_signals = []

        for m in range(M):
            shift = delay_samples[m]

            if shift == 0:
                aligned = mic_signals[m]
            else:
                aligned = mic_signals[m, shift:]

            aligned_signals.append(aligned)

        # Some length for every signal
        min_length = min(len(signal) for signal in aligned_signals)
        aligned_signals = np.array([signal[:min_length] for signal in aligned_signals])

        # Delay and sum
        beamformed_signal = np.sum(aligned_signals, axis = 0)

        # Beamforming power
        beam_map[iy, ix] = np.mean(beamformed_signal**2)

# NORMALIZE PSF
psf = beam_map/np.max(beam_map)

# POSITION OF MAXIMUM
max_index = np.unravel_index(np.argmax(psf), psf.shape)

estimated_y = y_scan[max_index[0]]
estimated_x = x_scan[max_index[1]]

print("True source:")
print(source_x, source_y)

print()

print("PSF maximum:")
print(estimated_x, estimated_y)

# PLOT PSF

plt.figure(figsize=(9, 7))

plt.imshow(
    psf,
    extent=[
        x_scan[0],
        x_scan[-1],
        y_scan[0],
        y_scan[-1]
    ],
    origin="lower",
    aspect="auto",
    vmin=0,
    vmax=1
)

plt.colorbar(
    label="Normalized beamformer response"
)

plt.scatter(
    source_x,
    source_y,
    marker="x",
    s=120,
    label="Point source"
)

plt.scatter(
    mic_x,
    mic_y,
    marker="^",
    label="Microphones"
)

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title(
    "MovingSourceArrayLab - Experiment 04\n"
    "Point Spread Function"
)

plt.legend()

plt.show()

# PLOT
# HORIZONTAL CUT THROUGH THE SOURCE

source_y_index = np.argmin(
    np.abs(y_scan - source_y)
)

horizontal_psf = psf[
    source_y_index,
    :
]

plt.figure(figsize=(9, 5))

plt.plot(
    x_scan,
    horizontal_psf
)

plt.axvline(
    source_x,
    linestyle="--",
    label="True source"
)

plt.xlabel("x [m]")
plt.ylabel("Normalized response")

plt.title(
    "Horizontal cut of the PSF at y = 1 m"
)

plt.grid()
plt.legend()

plt.show()

