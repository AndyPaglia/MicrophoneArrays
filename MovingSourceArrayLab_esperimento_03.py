# 03) FIRST 2D TIME-DOMAIN BEAMFORMING MAP

import numpy as np
import matplotlib.pyplot as plt

# FIXED PARAMETERS
c = 343.0 # m/s - sound velocity
fs = 48000 # sampling frequency
duration = 0.01 
f0 = 2000.0 

# MICROPHONE ARRAY
M = 8
d = 0.05

mic_x = (np.arange(M) - (M - 1)/2) * d
mic_y = np.zeros(M)

# TIME AXIS
N = int(duration*fs)
t = np.arange(N)/fs

# TRUE SOURCE POSITION
source_x = 0.30 
source_y = 1.00

# FINO A QUI ABBIAMO CREATO LA NOSTRA GEOMETRIA DELL'ARRAY E DELLA SORGENTE

# TRUE PROPAGATION DELAYS
distances = np.sqrt((source_x - mic_x)**2 + (source_y - mic_y)**2) # distance mics-source
arrival_times = distances/c # source time of arrival for each mic
relative_delays = arrival_times - np.min(arrival_times) # relative delays between ref mic and other mics

# SIMULATED MICROPHONE SIGNALS
mic_signals = np.zeros((M, N)) # matrice di zeri con M righe e N colonne che conterrà il segnale ricevuto
# dai microfoni

# per ogni microfono prendo il suo specifico delay
# inserisco in mic_signals lo stesso segnale della sorgente ma traslato di tau quindi del delay
# specifico di quel microfono
# Questo perchè ogni microgono riceve lo stesso segnale sinusoidale ma ritardato di tauM
for m in range(M):
    tau = relative_delays[m]
    mic_signals[m, :] = np.sin(2 * np.pi * f0 * (t - tau))

# SCANNING GRID
# Proviamo molti punti (x,y) nello spazio.
# Per ogni punto calcoliamo i ritardi che avremmo se la sorgente fosse li
x_scan = np.linspace(-1.0, 1.0, 81)
y_scan = np.linspace(0.2, 2.0, 81)

beam_map = np.zeros((len(y_scan), len(x_scan)))

# TIME-DOMAIN BEAMFORMING
# For every point in the map (x,y), calculate the delays that we would have had if a source 
# would have been there

# Per ogni punt (x, y)
# Calcoliamo i ritardi attesi
# Convertiamo in campioni
# Riallineaiamo i segnali
# Li sommiamo e calcoliamo la potenza

for iy, y in enumerate(y_scan):
    for ix, x in enumerate(x_scan):
        # expected distances from this scan point
        scan_distances = np.sqrt((x - mic_x)**2 + (y - mic_y)**2)

        # expected propagation times
        scan_times = scan_distances/c

        # relative to the nearest microphone
        scan_delays = scan_times - np.min(scan_times)

        # convert delays into integer samples
        delay_samples = np.round(scan_delays*fs).astype(int)

        # align the microphone signals
        aligned_signals = []

        # qui quindi io prendo per ogni microfono, il delay effettivo che ha
        # con la sorgente ipotizzata dentro la grid map
        # in base a quel delay io vado a prendere il segnale trovato sopra reale per ogni microfono
        # e sposto quell'array iniziandolo da dopo i campioni di shift quidni è come se tagliassi
        # un pezzo del segnale, che può coincidere con il segnale originale o no
        # dipende dalla posizione se è giusta o meno
        for m in range(M):
            shift = delay_samples[m]
            if shift == 0:
                aligned = mic_signals[m]
            else:
                aligned = mic_signals[m, shift:]

            aligned_signals.append(aligned)


        # all signals must have same length
        min_length = min(len(signal) for signal in aligned_signals)
        # taglio una parte dei segnali perchè sennò avrebbero lunghezza differente
        aligned_signals = np.array([signal[:min_length] for signal in aligned_signals])

        # sum the aligned microphone signals
        beamformed_signal = np.sum(aligned_signals, axis = 0)

        # beamformer power
        beam_map[iy, ix] = np.mean(beamformed_signal**2)

# ESTIMATED SOURCE POSITION
max_index = np.unravel_index(np.argmax(beam_map), beam_map.shape)

estimated_y = y_scan[max_index[0]]
estimated_x = x_scan[max_index[1]]

print()
print("True source position:")
print(source_x, source_y)

print()
print("Estimated source position:")
print(estimated_x, estimated_y)

# PLOT
plt.figure(figsize=(9, 7))
for i in range(M):
    plt.plot([source_x, mic_x[i]], [source_y, mic_y[i]], linestyle = "--", alpha = 0.4)

# Microphones
plt.scatter(mic_x, mic_y, label = "Microphones")
plt.scatter(source_x, source_y, marker = "x", s = 100, label = "source")

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Source - Microphone Array Geometry")

plt.grid()
plt.axis("equal")
plt.legend()

# IMPORTANT: actually display the plot
plt.show()

# PLOT

plt.figure(figsize=(9, 7))

# ogni elemento della beam map rappresenta la potenza ottenuta dal beamformer quando ipotizzo che 
# la sorgente si trovi nel punto (x_scan[ix]. y_scan [iy])
plt.imshow(
    beam_map,
    extent=[
        x_scan[0],
        x_scan[-1],
        y_scan[0],
        y_scan[-1]
    ],
    origin="lower",
    aspect="auto"
)

plt.colorbar(
    label="Beamformer power"
)

plt.scatter(
    source_x,
    source_y,
    marker="x",
    s=100,
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
    "MovingSourceArrayLab - Experiment 03\n"
    "First 2D time-domain beamforming map"
)

plt.legend()
plt.show()