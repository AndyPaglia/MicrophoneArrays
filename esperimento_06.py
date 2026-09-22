# 6) DELAY AND SUM BEAMFORMING

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI
c = 343.0 # m/s
f0 = 1000 # Hz
theta_true_deg = 20.0 # gradi
M = 8
d = 0.08 # metri

# GEOMETRIA ARRAY
mic_x = (np.arange(M) - (M - 1) / 2) * d
print("Microfoni:")
print(mic_x)

# DIREZIONE REALE SORGENTE
theta_true = np.deg2rad(theta_true_deg)

# Ritardi relativi reali
tau_true = (mic_x * np.sin(theta_true) / c)

# SEGNALE OSSERVATO DAI MICROFONI
X = np.exp(-1j * 2 * np.pi * f0 * tau_true)

rng = np.random.default_rng(42)
noise_level = 0.5
noise = (rng.normal(0, noise_level, M) + 1j * rng.normal(0, noise_level, M))
X = X + noise

print()
print("Segnale complesso sui microfoni:")
print(X)

# ANGOLI DA TESTARE
scan_angles_deg = np.linspace(-90, 90, 361)

beam_output = []

# SCANSIONE ANGOLARE
for theta_deg in scan_angles_deg:

    theta = np.deg2rad(theta_deg)

    # ritardi previsti per questo angolo 
    tau_scan = (mic_x * np.sin(theta) / c)

    # steering vector

    steering = np.exp(-1j * 2 * np.pi * f0 * tau_scan)

    # compensazione + somma

    y = np.vdot(steering, X)

    power = np.abs(y)**2

    beam_output.append(power)

beam_output = np.array(beam_output)

# NORMALIZZAZIONE
beam_output = beam_output / np.max(beam_output)

beam_db = 10 * np.log10(beam_output + 1e-12)

# TROVIAMO IL MASSIMO
max_index = np.argmax(beam_output)

estimated_angle = scan_angles_deg[max_index]

print()
print(
    "Angolo reale:",
    theta_true_deg,
    "gradi"
)

print(
    "Angolo stimato:",
    estimated_angle,
    "gradi"
)

# GRAFICO
plt.figure(figsize=(10, 5))

plt.plot(
    scan_angles_deg,
    beam_output
)

plt.axvline(
    theta_true_deg,
    linestyle="--",
    label="Angolo reale"
)

plt.axvline(
    estimated_angle,
    linestyle=":",
    label="Angolo stimato"
)

plt.xlabel("Angolo [gradi]")
plt.ylabel("Potenza normalizzata")

plt.title(
    "Delay-and-Sum Beamforming"
)

plt.grid()
plt.legend()

plt.show()

plt.figure(figsize=(10, 5))

plt.plot(
    scan_angles_deg,
    beam_db
)

plt.xlabel("Angolo [gradi]")
plt.ylabel("Livello [dB]")

plt.title("Beam pattern")

plt.ylim(-40, 0)

plt.grid()

plt.show()