# 10) CROSS-SPECTRAL MATRIX + NEAR-FIELD BEAMFORMING

import numpy as np
import matplotlib.pyplot as plt


# ==========================================
# PARAMETRI FISICI
# ==========================================

c = 343.0              # velocità del suono [m/s]
fs = 48000             # sampling rate [Hz]
f0 = 2000.0            # frequenza sorgente [Hz]

duration = 1.0         # durata segnale [s]

M = 8                  # numero microfoni
d = 0.05               # spacing [m]


# ==========================================
# GEOMETRIA ARRAY
# ==========================================

mic_x = (
    np.arange(M) - (M - 1) / 2
) * d

mic_y = np.zeros(M)

print("Posizioni microfoni x:")
print(mic_x)


# ==========================================
# POSIZIONE REALE SORGENTE
# ==========================================

source_x = 0.30
source_y = 1.00

print()
print("Posizione reale sorgente:")
print("x =", source_x, "m")
print("y =", source_y, "m")


# ==========================================
# ASSE TEMPORALE
# ==========================================

N = int(duration * fs)

t = np.arange(N) / fs


# ==========================================
# DISTANZE SORGENTE -> MICROFONI
# ==========================================

r_true = np.sqrt(
    (source_x - mic_x)**2
    +
    (source_y - mic_y)**2
)

print()
print("Distanze sorgente -> microfoni:")
print(r_true)


# ==========================================
# TEMPI DI PROPAGAZIONE
# ==========================================

tau_true = r_true / c

print()
print("Tempi di propagazione [ms]:")
print(tau_true * 1000)


# ==========================================
# SEGNALI AI MICROFONI
# ==========================================

signals = np.zeros(
    (M, N)
)

for m in range(M):

    signals[m] = np.sin(
        2 * np.pi * f0 * (t - tau_true[m])
    )


# ==========================================
# AGGIUNGIAMO RUMORE
# ==========================================

rng = np.random.default_rng(42)

noise_level = 0.5

noise = rng.normal(
    0,
    noise_level,
    size=signals.shape
)

signals_noisy = signals + noise


# ==========================================
# PARAMETRI FFT A BLOCCHI
# ==========================================

block_size = 2048
hop_size = 1024

window = np.hanning(
    block_size
)


# ==========================================
# ASSE DELLE FREQUENZE FFT
# ==========================================

freqs = np.fft.rfftfreq(
    block_size,
    d=1 / fs
)


# ==========================================
# BIN FFT PIU VICINO A f0
# ==========================================

index_f0 = np.argmin(
    np.abs(freqs - f0)
)

f_bin = freqs[index_f0]

print()
print("Frequenza desiderata =", f0, "Hz")
print("Bin FFT utilizzato =", f_bin, "Hz")


# ==========================================
# NUMERO D'ONDA
# ==========================================

k = 2 * np.pi * f_bin / c

print()
print("Numero d'onda k =", k, "rad/m")


# ==========================================
# INIZIALIZZIAMO LA CSM
# ==========================================

CSM = np.zeros(
    (M, M),
    dtype=complex
)

num_blocks = 0


# ==========================================
# COSTRUZIONE DELLA CSM
# ==========================================

for start in range(
    0,
    N - block_size + 1,
    hop_size
):

    end = start + block_size

    # blocco di tutti i microfoni
    block = signals_noisy[
        :,
        start:end
    ]

    # applichiamo finestra Hann
    block = block * window

    # FFT lungo il tempo
    X_fft = np.fft.rfft(
        block,
        axis=1
    )

    # prendiamo solo il bin vicino a f0
    X = X_fft[
        :,
        index_f0
    ]

    # ======================================
    # CSM DEL BLOCCO
    #
    # X X^H
    # ======================================

    CSM_block = np.outer(
        X,
        np.conj(X)
    )

    CSM += CSM_block

    num_blocks += 1


# ==========================================
# MEDIA TRA I BLOCCHI
# ==========================================

CSM /= num_blocks

print()
print("Numero blocchi =", num_blocks)

print()
print("Shape CSM =", CSM.shape)


# ==========================================
# CONTROLLO HERMITIANO
# ==========================================

hermitian_error = np.max(
    np.abs(
        CSM - np.conj(CSM.T)
    )
)

print()
print(
    "Errore Hermitiano CSM =",
    hermitian_error
)


# ==========================================
# VISUALIZZIAMO IL MODULO DELLA CSM
# ==========================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    np.abs(CSM),
    origin="upper"
)

plt.colorbar(
    label="|CSM|"
)

plt.xlabel("Microfono j")
plt.ylabel("Microfono i")

plt.title(
    f"Modulo della CSM a {f_bin:.1f} Hz"
)

plt.show()


# ==========================================
# GRIGLIA DI SCANSIONE
# ==========================================

x_scan = np.linspace(
    -1.0,
    1.0,
    161
)

y_scan = np.linspace(
    0.2,
    2.0,
    161
)

beam_map = np.zeros(
    (
        len(y_scan),
        len(x_scan)
    )
)


# ==========================================
# BEAMFORMING NEAR FIELD
# ==========================================

for iy, y in enumerate(y_scan):

    for ix, x in enumerate(x_scan):

        # ==================================
        # DISTANZE DEL PUNTO CANDIDATO
        # ==================================

        r_scan = np.sqrt(
            (x - mic_x)**2
            +
            (y - mic_y)**2
        )

        # ==================================
        # DISTANZE RELATIVE
        # ==================================

        # usiamo mic 0 come riferimento

        delta_r_scan = (
            r_scan - r_scan[0]
        )

        # ==================================
        # STEERING VECTOR
        # ==================================
        #
        # a_m = exp(-j k delta_r_m)
        #

        steering = np.exp(
            -1j
            * k
            * delta_r_scan
        )

        # ==================================
        # BEAMFORMER
        #
        # P = a^H C a
        # ==================================

        power = (
            np.conj(steering)
            @ CSM
            @ steering
        )

        # teoricamente reale
        power = np.real(power)

        # evitiamo piccoli valori negativi
        # dovuti a precisione numerica
        if power < 0:
            power = 0.0

        beam_map[
            iy,
            ix
        ] = power


# ==========================================
# TEST DIRETTO NELLA POSIZIONE REALE
# ==========================================

r_test = np.sqrt(
    (source_x - mic_x)**2
    +
    (source_y - mic_y)**2
)

delta_r_test = (
    r_test - r_test[0]
)

steering_test = np.exp(
    -1j
    * k
    * delta_r_test
)

power_at_true_position = np.real(
    np.conj(steering_test)
    @ CSM
    @ steering_test
)

print()
print(
    "Potenza nella posizione reale =",
    power_at_true_position
)


# ==========================================
# MASSIMO PRIMA DELLA NORMALIZZAZIONE
# ==========================================

max_power = np.max(
    beam_map
)

print(
    "Potenza massima della mappa =",
    max_power
)


# ==========================================
# POSIZIONE DEL MASSIMO
# ==========================================

max_index = np.unravel_index(
    np.argmax(beam_map),
    beam_map.shape
)

estimated_y = y_scan[
    max_index[0]
]

estimated_x = x_scan[
    max_index[1]
]


print()
print("==============================")
print("RISULTATO LOCALIZZAZIONE")
print("==============================")

print()

print(
    "Posizione reale:",
    source_x,
    source_y
)

print(
    "Posizione stimata:",
    estimated_x,
    estimated_y
)


# ==========================================
# ERRORE DI LOCALIZZAZIONE
# ==========================================

localization_error = np.sqrt(
    (estimated_x - source_x)**2
    +
    (estimated_y - source_y)**2
)

print(
    "Errore di localizzazione:",
    localization_error,
    "m"
)


# ==========================================
# DIAGNOSTICA MAPPA
# ==========================================

print()
print("==============================")
print("DIAGNOSTICA MAPPA")
print("==============================")

print()

print(
    "beam_map min =",
    np.min(beam_map)
)

print(
    "beam_map max =",
    np.max(beam_map)
)

print(
    "NaN presenti =",
    np.isnan(beam_map).any()
)

print(
    "Inf presenti =",
    np.isinf(beam_map).any()
)

print(
    "Valori negativi =",
    np.sum(beam_map < 0)
)


# ==========================================
# NORMALIZZAZIONE
# ==========================================

if max_power > 0:

    beam_map_normalized = (
        beam_map / max_power
    )

else:

    beam_map_normalized = beam_map.copy()


# ==========================================
# CONVERSIONE IN dB
# ==========================================

beam_map_db = 10 * np.log10(
    beam_map_normalized + 1e-12
)


# ==========================================
# GRAFICO 1
# GEOMETRIA
# ==========================================

plt.figure(
    figsize=(9, 6)
)

plt.scatter(
    mic_x,
    mic_y,
    s=80,
    label="Microfoni"
)

plt.scatter(
    source_x,
    source_y,
    marker="x",
    s=140,
    linewidths=3,
    label="Sorgente reale"
)

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title(
    "Geometria array e sorgente"
)

plt.grid()
plt.legend()

plt.xlim(-1, 1)
plt.ylim(-0.1, 2)

plt.show()


# ==========================================
# GRAFICO 2
# MODULO DELLA CSM
# ==========================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    np.abs(CSM)
)

plt.colorbar(
    label="|CSM|"
)

plt.xlabel("Microfono j")
plt.ylabel("Microfono i")

plt.title(
    f"Modulo della CSM a {f_bin:.1f} Hz"
)

plt.show()


# ==========================================
# GRAFICO 3
# ACOUSTIC MAP LINEARE
# ==========================================

plt.figure(
    figsize=(9, 7)
)

plt.imshow(
    beam_map_normalized,
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
    label="Potenza normalizzata"
)

plt.scatter(
    source_x,
    source_y,
    marker="x",
    s=150,
    linewidths=3,
    label="Sorgente reale"
)

plt.scatter(
    estimated_x,
    estimated_y,
    marker="+",
    s=180,
    linewidths=3,
    label="Sorgente stimata"
)

plt.scatter(
    mic_x,
    mic_y,
    marker="o",
    s=50,
    label="Microfoni"
)

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title(
    f"Near-field Beamforming CSM - {f_bin:.1f} Hz"
)

plt.legend()

plt.show()


# ==========================================
# GRAFICO 4
# ACOUSTIC MAP IN dB
# ==========================================

plt.figure(
    figsize=(9, 7)
)

plt.imshow(
    beam_map_db,
    extent=[
        x_scan[0],
        x_scan[-1],
        y_scan[0],
        y_scan[-1]
    ],
    origin="lower",
    aspect="auto",
    vmin=-20,
    vmax=0
)

plt.colorbar(
    label="Livello [dB]"
)

plt.scatter(
    source_x,
    source_y,
    marker="x",
    s=150,
    linewidths=3,
    label="Sorgente reale"
)

plt.scatter(
    estimated_x,
    estimated_y,
    marker="+",
    s=180,
    linewidths=3,
    label="Sorgente stimata"
)

plt.scatter(
    mic_x,
    mic_y,
    marker="o",
    s=50,
    label="Microfoni"
)

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title(
    f"Acoustic Map CSM [dB] - {f_bin:.1f} Hz"
)

plt.legend()

plt.show()