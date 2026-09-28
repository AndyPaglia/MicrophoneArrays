# 09) NEAR FIELD VS FAR FIELD
# LOCALIZZAZIONE 2D CON DELAY-AND-SUM

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI FISICI

c = 343.0          # velocità del suono [m/s]
f0 = 2000.0        # frequenza della sorgente [Hz]

# PARAMETRI ARRAY

M = 8              # numero di microfoni
d = 0.05           # distanza tra microfoni [m]

# GEOMETRIA ARRAY

# Array lineare centrato in x = 0
mic_x = (np.arange(M) - (M - 1) / 2) * d
mic_y = np.zeros(M)

print("Posizioni microfoni x [m]:")
print(mic_x)

# Apertura totale array
D = (M - 1) * d

print()
print("Apertura array D =", D, "m")

# POSIZIONE REALE DELLA SORGENTE

source_x = 0.30
source_y = 1.00

print()
print("Posizione reale sorgente:")
print("x =", source_x, "m")
print("y =", source_y, "m")

# LUNGHEZZA D'ONDA E NUMERO D'ONDA

wavelength = c / f0

k = 2 * np.pi / wavelength

print()
print("Lunghezza d'onda =", wavelength, "m")
print("Numero d'onda k =", k, "rad/m")

# DISTANZE SORGENTE -> MICROFONI
r_true = np.sqrt((source_x - mic_x)**2 + (source_y - mic_y)**2)

print()
print("Distanze sorgente -> microfoni [m]:")
print(r_true)

# TEMPI DI ARRIVO
t_true = r_true / c

print()
print("Tempi di arrivo [ms]:")
print(t_true * 1000)

# DISTANZE RELATIVE

# Usiamo il primo microfono come riferimento

r_ref = r_true[0]
delta_r_true = r_true - r_ref

print()
print("Differenze di percorso rispetto a Mic 0 [m]:")
print(delta_r_true)

# RITARDI RELATIVI
tau_true = delta_r_true / c

print()
print("Ritardi relativi [microsecondi]:")
print(tau_true * 1e6)

# SEGNALE COMPLESSO OSSERVATO

# Qui simuliamo ciò che ciascun microfono osserva
# alla frequenza f0.
# Ogni microfono ha una fase diversa a causa
# della diversa distanza dalla sorgente.

X = np.exp( -1j * k * delta_r_true)

print()
print("Segnale complesso sui microfoni:")
print(X)

# FASI OSSERVATE

phase_true = np.angle(X)

phase_true_deg = np.degrees(phase_true)

print()
print("Fasi osservate [gradi]:")
print(phase_true_deg)

# GRIGLIA DI SCANSIONE

# Cerchiamo la sorgente in questa regione

x_scan = np.linspace(-1.0, 1.0, 161)

y_scan = np.linspace(0.2, 2.0, 161)

# Matrice che conterrà la potenza beamformer

beam_map = np.zeros((len(y_scan), len(x_scan)))

# BEAMFORMING NEAR FIELD 2D

for iy, y in enumerate(y_scan):

    for ix, x in enumerate(x_scan):

        # DISTANZA DEL PUNTO CANDIDATO
        # DA OGNI MICROFONO
        r_scan = np.sqrt((x - mic_x)**2 + (y - mic_y)**2)

        # DISTANZE RELATIVE
        delta_r_scan = (r_scan - r_scan[0])

        # STEERING VECTOR
        steering = np.exp(-1j * k * delta_r_scan)

        # DELAY-AND-SUM
        # np.vdot fa:
        # conjugate(steering) dot X
        # cioè:
        # steering^H X

        y_beam = np.vdot(steering, X)

        # POTENZA

        beam_map[iy, ix] = (np.abs(y_beam)**2)

# NORMALIZZAZIONE
beam_map = (beam_map / np.max(beam_map))

# TROVIAMO IL MASSIMO

max_index = np.unravel_index(np.argmax(beam_map), beam_map.shape)

estimated_y = y_scan[max_index[0]]

estimated_x = x_scan[max_index[1]]

print()
print("RISULTATO LOCALIZZAZIONE")

print()

print("Posizione reale:", source_x, source_y)

print("Posizione stimata:", estimated_x, estimated_y)

# ERRORE DI LOCALIZZAZIONE

localization_error = np.sqrt((estimated_x - source_x)**2 +(estimated_y - source_y)**2)

print("Errore di localizzazione:", localization_error, "m")

# GRAFICO 1
# GEOMETRIA
plt.figure(figsize=(9, 6))

plt.scatter(mic_x, mic_y, s=100, label="Microfoni")

plt.scatter(source_x, source_y, marker="*", s=200, label="Sorgente")

# Colleghiamo sorgente e microfoni

for m in range(M):

    plt.plot([source_x, mic_x[m]],[source_y, mic_y[m]], "--", alpha=0.4)

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title("Geometria array - Near Field")

plt.axis("equal")
plt.grid()
plt.legend()

plt.show()

# GRAFICO 2
# FASE SUI MICROFONI

plt.figure(figsize=(9, 5))

plt.plot(mic_x, phase_true_deg, "o-")

plt.xlabel("Posizione microfono x [m]")

plt.ylabel("Fase [gradi]")

plt.title("Fase osservata sui microfoni")

plt.grid()

plt.show()

# GRAFICO 3
# ACOUSTIC MAP

plt.figure(figsize=(9, 7))

plt.imshow(beam_map, extent=[x_scan[0], x_scan[-1], y_scan[0], y_scan[-1]], origin="lower", aspect="auto")

plt.colorbar(label="Potenza normalizzata")

# SORGENTE REALE

plt.scatter(source_x, source_y, marker="x", s=120, linewidths=3, label="Sorgente reale")

# MASSIMO TROVATO

plt.scatter(estimated_x, estimated_y, marker="+", s=180, linewidths=3, label="Posizione stimata")

# MICROFONI

plt.scatter(mic_x, mic_y, marker="o", s=60, label="Microfoni")

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Near-Field Delay-and-Sum Acoustic Map")
plt.legend()
plt.show()

# GRAFICO 4
# ACOUSTIC MAP IN dB

beam_map_db = 10 * np.log10(beam_map + 1e-12)

plt.figure(figsize=(9, 7))

plt.imshow(beam_map_db, extent=[x_scan[0], x_scan[-1], y_scan[0], y_scan[-1]],origin="lower", aspect="auto", vmin=-30, vmax=0)

plt.colorbar(label="Livello [dB]")

plt.scatter(source_x, source_y, marker="x", s=120, linewidths=3, label="Sorgente reale")

plt.scatter(estimated_x, estimated_y, marker="+", s=180, linewidths=3, label="Posizione stimata")

plt.scatter(mic_x, mic_y, marker="o", s=60, label="Microfoni")

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Near-Field Acoustic Map [dB]")
plt.legend()
plt.show()

# DISTANZA DI FRAUNHOFER

fraunhofer_distance = (2 * D**2 / wavelength)

print()
print("NEAR FIELD / FAR FIELD")

print()
print("Distanza di Fraunhofer ≈", fraunhofer_distance, "m")

source_distance_from_center = np.sqrt(source_x**2 + source_y**2)

print("Distanza sorgente dal centro array ≈", source_distance_from_center, "m")

if source_distance_from_center < fraunhofer_distance:

    print(
        "La sorgente si trova circa "
        "nella regione near-field."
    )

else:

    print(
        "La sorgente si trova circa "
        "nella regione far-field."
    )