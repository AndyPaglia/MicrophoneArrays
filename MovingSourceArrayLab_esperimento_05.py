# 05) BROADBAND SOURCE + FRACTIONAL DELAYS

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt

# FIXED PARAMETERS
c = 343.0
fs = 48000
duration = 0.05

# MICROPHONE ARRAY

M = 8
d = 0.05

mic_x = (np.arange(M) - (M - 1) / 2) * d
mic_y = np.zeros(M)

# TRUE SOURCE POSITION

source_x = 0.30
source_y = 1.00

# TIME AXIS

N = int(duration * fs)

t = np.arange(N) / fs

# BROADBAND SOURCE SIGNAL

rng = np.random.default_rng(42) # generazione numeri randomici

white_noise = rng.standard_normal(N) # creazione di una distribuzione normale di N campioni

# Band-pass filter:
# keep approximately 500 - 4000 Hz
# applichiamo un filtro. Manteniamo le frequenza da 500 Hz a 4000 Hz. Abbiamo un segnale broadband.
sos = butter(
    4,
    [500, 4000],
    btype="bandpass",
    fs=fs,
    output="sos"
)

source_signal = sosfiltfilt(
    sos,
    white_noise
)

# normalize
source_signal = (
    source_signal /
    np.max(np.abs(source_signal))
)

# TRUE SOURCE -> MICROPHONE DELAYS

distances = np.sqrt(
    (source_x - mic_x)**2 +
    (source_y - mic_y)**2
)

arrival_times = distances / c

relative_delays = (
    arrival_times -
    np.min(arrival_times)
)

# SIMULATE MICROPHONE SIGNALS
# USING FRACTIONAL DELAYS

mic_signals = np.zeros((M, N))

for m in range(M):

    tau = relative_delays[m]

    delayed_time = t - tau

# np.interp mantiene il numero in virgola. Ci permette di chiedere il valore  del segnale anche tra due campioni

    mic_signals[m] = np.interp(
        delayed_time,
        t,
        source_signal,
        left=0,
        right=0
    )
# left = 0, right = 0 fanno si che i valori non vadano al di fuori dei limiti dello studio

# PRINT DELAYS

print()
print("Relative delays [microseconds]:")

print(
    relative_delays * 1e6
)

print()
print("Relative delays [samples]:")

print(
    relative_delays * fs
)

# PLOT SOURCE AND SOME MICROPHONE SIGNALS

plt.figure(figsize=(10, 6))

plt.plot(
    t * 1000,
    source_signal,
    label="Source",
    alpha=0.8
)

plt.plot(
    t * 1000,
    mic_signals[0],
    label="Mic 0"
)

plt.plot(
    t * 1000,
    mic_signals[7],
    label="Mic 7"
)

plt.xlim(0, 5)

plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")

plt.title(
    "Broadband source and delayed microphone signals"
)

plt.grid()
plt.legend()

plt.show()

# SCANNING GRID

x_scan = np.linspace(
    -1.0,
    1.0,
    81
)

y_scan = np.linspace(
    0.2,
    2.0,
    81
)

beam_map = np.zeros(
    (
        len(y_scan),
        len(x_scan)
    )
)

# TIME-DOMAIN BEAMFORMING

for iy, y in enumerate(y_scan):

    for ix, x in enumerate(x_scan):

        # --------------------------------------------
        # Expected distances if source were here
        # --------------------------------------------

        scan_distances = np.sqrt(
            (x - mic_x)**2 +
            (y - mic_y)**2
        )

        # --------------------------------------------
        # Expected propagation times
        # --------------------------------------------

        scan_times = (
            scan_distances / c
        )

        # --------------------------------------------
        # Relative expected delays
        # --------------------------------------------

        scan_delays = (
            scan_times -
            np.min(scan_times)
        )

        # --------------------------------------------
        # Fractional-delay alignment
        # --------------------------------------------

        aligned_signals = np.zeros(
            (M, N)
        )

        for m in range(M):

            tau = scan_delays[m]

            # We ADVANCE the microphone signal
            # by the hypothesized delay.
            #
            # x_m(t + tau)

            shifted_time = (
                t + tau
            )

            aligned_signals[m] = np.interp(
                shifted_time,
                t,
                mic_signals[m],
                left=0,
                right=0
            )

        # --------------------------------------------
        # Avoid edge regions created by interpolation
        # --------------------------------------------

        max_delay = np.max(
            scan_delays
        )

        start = 0

        end = N - int(
            np.ceil(max_delay * fs)
        ) - 1

        if end <= start:
            continue

        valid_signals = aligned_signals[
            :,
            start:end
        ]

        # --------------------------------------------
        # Delay-and-sum
        # --------------------------------------------

        beamformed_signal = np.sum(
            valid_signals,
            axis=0
        )

        # --------------------------------------------
        # Beamformer power
        # --------------------------------------------

        beam_map[iy, ix] = np.mean(
            beamformed_signal**2
        )

# NORMALIZATION

beam_map_normalized = (
    beam_map /
    np.max(beam_map)
)

# FIND MAXIMUM

max_index = np.unravel_index(
    np.argmax(beam_map_normalized),
    beam_map_normalized.shape
)

estimated_y = (
    y_scan[max_index[0]]
)

estimated_x = (
    x_scan[max_index[1]]
)


print()
print("True source position:")

print(
    source_x,
    source_y
)

print()
print("Estimated source position:")

print(
    estimated_x,
    estimated_y
)

# BEAMFORMING MAP
plt.figure(figsize=(9, 7))

plt.imshow(
    beam_map_normalized,
    extent=[
        x_scan[0],
        x_scan[-1],
        y_scan[0],
        y_scan[-1]
    ],
    origin="lower",
    aspect="equal",
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
    label="True source"
)

plt.scatter(
    estimated_x,
    estimated_y,
    marker="o",
    facecolors="none",
    s=120,
    label="Estimated source"
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
    "MovingSourceArrayLab - Experiment 05\n"
    "Broadband fractional-delay beamforming"
)

plt.legend()

plt.show()