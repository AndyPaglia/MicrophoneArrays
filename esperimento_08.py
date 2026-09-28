# 8) SPATIAL ALIASING AND GRATING LOBES

# Se d > lambda/2 potrebbero comparire grating lobes
# d deve essere minore di lambda/2
# d < c/2f
# f_alias = c/2d

import numpy as np
import matplotlib.pyplot as plt

# COSTANTI
c = 343.0

# FUNZIONE BEAM PATTERN

def beam_pattern(M, d, f0):

    # posizioni microfoni
    mic_x = (np.arange(M) - (M - 1) / 2) * d

    # direzione verso cui puntiamo
    theta0_deg = 0.0
    theta0 = np.deg2rad(theta0_deg)

    # steering vector della direzione desiderata
    tau0 = (mic_x * np.sin(theta0) / c)

    steering0 = np.exp(-1j * 2 * np.pi * f0 * tau0)

    # angoli da analizzare
    angles_deg = np.linspace(-90, 90, 2001)




    response = []

    for angle_deg in angles_deg:

        theta = np.deg2rad(angle_deg)

        tau = (mic_x  * np.sin(theta) / c)

        steering = np.exp(-1j * 2 * np.pi * f0 * tau)

        y = np.vdot(steering0, steering)

        power = np.abs(y)**2

        response.append(power)

    response = np.array(response)

    response /= np.max(response)

    response_db = 10 * np.log10(
        response + 1e-12
    )

    return angles_deg, response_db

# PARAMETRI ARRAY
M = 8
d = 0.05

alias_frequency = c / (2 * d)

print("Frequenza limite:", alias_frequency,"Hz")

# CONFRONTO FREQUENZE

frequencies = [
    1000,
    3000,
    4000,
    5000,
    8000
]

# Figure differenti in base a differenti frequenze
plt.figure(figsize=(11, 6))

for f0 in frequencies:

    angles, pattern = beam_pattern(
        M,
        d,
        f0
    )

    plt.plot(
        angles,
        pattern,
        label=f"{f0} Hz"
    )


plt.xlabel("Angolo [gradi]")
plt.ylabel("Risposta [dB]")

plt.title(
    "Spatial aliasing al variare della frequenza"
)

plt.ylim(-40, 1)
plt.xlim(-90, 90)

plt.grid()
plt.legend()

plt.show()

# Figures con differenti d
f0 = 1000

spacings = [
    0.05,
    0.10,
    0.20,
    0.30
]

plt.figure(figsize=(11, 6))

for d_test in spacings:

    angles, pattern = beam_pattern(
        M=8,
        d=d_test,
        f0=1000
    )

    plt.plot(
        angles,
        pattern,
        label=f"d = {d_test} m"
    )

plt.xlabel("Angolo [gradi]")
plt.ylabel("Risposta [dB]")

plt.title(
    "Spatial aliasing al variare di d"
)

plt.ylim(-40, 1)
plt.xlim(-90, 90)

plt.grid()
plt.legend()

plt.show()