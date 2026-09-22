# 5) 8 MIC ARRAY AND STEERING VECTOR

# Costruiamo un array lineare con 8 microfoni
# se una sorgente arriva da un certo angolo, quale differenza di fase deve comparire sui vari microfoni? --> STEERING VECTOR

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI
c = 343.0 # velocità della luce
f0 = 1000.0
M = 8 # 8 microfoni
d = 0.05

theta_deg = 30.0

# GEOMETRIA ARRAY
mic_x = (np.arange(M) - (M-1) / 2) * d # np.arange(M) * d da l'array delle posizioni dei microfoni ma noi lo vogliamo centrato su 0 quindi sottranedo la lunghezza dei microfoni (M-1)*d diviso 2

print("Posizioni microfoni [m]:")
print(mic_x)

# apertura array

D = (M - 1) * d

print()
print("Apertura array =", D, "m")

# FREQUENZA E NUMERO D'ONDA
wavelength = c/f0
k = 2 * np.pi / wavelength

print()
print("Lunghezza d'onda =", wavelength, "m")
print("Numero d'onda k =", k, "rad/m")

# ANGOLO
theta = np.deg2rad(theta_deg)

# RITARDI
tau = mic_x * np.sin(theta) / c

print()
print("Ritardi relativi [microsecondi]:")

print(tau * 1e6)

# STEERING VECTOR
steering = np.exp(-1j * 2 * np.pi * f0 * tau)

print()
print("Steering vector:")
print(steering)

# FASE DELLO STEERING VECTOR
phase = np.angle(steering)
phase_deg = np.degrees(phase)

print()
print("Fasi [gradi]:")
print(phase_deg)

# GRAFICO FASE

plt.figure(figsize=(9, 5))

plt.plot(mic_x, phase_deg, "o-")

plt.xlabel("Posizione microfono x [m]")
plt.ylabel("Fase [gradi]")

plt.title(f"Steering vector - theta = {theta_deg}°")

plt.grid()

plt.show()

angles_deg = [
    -60,
    -30,
    0,
    30,
    60
]

plt.figure(figsize=(10, 6))

for angle_deg in angles_deg:

    angle = np.deg2rad(angle_deg)

    tau_angle = (
        mic_x
        * np.sin(angle)
        / c
    )

    steering_angle = np.exp(
        -1j
        * 2
        * np.pi
        * f0
        * tau_angle
    )

    phase_angle = np.degrees(
        np.angle(steering_angle)
    )

    plt.plot(
        mic_x,
        phase_angle,
        "o-",
        label=f"{angle_deg}°"
    )

plt.xlabel("x [m]")
plt.ylabel("Fase [gradi]")

plt.title(
    "Steering vector per diverse direzioni"
)

plt.grid()
plt.legend()

plt.show()



