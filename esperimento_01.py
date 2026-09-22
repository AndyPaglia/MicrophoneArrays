# 1) 1 SOURCE + 2 MICROPHONES --> TOA AND TDOA CALCULATION

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI

c = 343.0  # velocità del suono [m/s]

# Microfoni
mic1 = np.array([-0.1, 0.0])
mic2 = np.array([ 0.1, 0.0])

# Sorgente
source = np.array([-0.6, 1.0])

# DISTANZE

r1 = np.linalg.norm(source - mic1)
r2 = np.linalg.norm(source - mic2)


# dx = source[0] - mic1[0]
# dy = source[1] - mic1[1]

# r1 = np.sqrt(dx**2 + dy**2)

# TEMPI DI ARRIVO

t1 = r1 / c
t2 = r2 / c

tdoa = t1 - t2

# RISULTATI

print("Distanza sorgente -> mic1:", r1, "m")
print("Distanza sorgente -> mic2:", r2, "m")

print()

print("Tempo arrivo mic1:", t1, "s")
print("Tempo arrivo mic2:", t2, "s")

print()

print("TDOA:", tdoa, "s")
print("TDOA:", tdoa * 1000, "ms")
print("TDOA:", tdoa * 1e6, "microsecondi")

# GRAFICO GEOMETRIA

plt.figure(figsize=(7, 6))

plt.scatter(mic1[0], mic1[1], s=100, label="Mic 1") # Coordinate, dimensioni punti e label
plt.scatter(mic2[0], mic2[1], s=100, label="Mic 2")
plt.scatter(source[0], source[1], s=150, marker="*", label="Sorgente")

plt.plot(
    [source[0], mic1[0]],
    [source[1], mic1[1]],
    "--"
)

plt.plot(
    [source[0], mic2[0]],
    [source[1], mic2[1]],
    "--"
)

plt.text(mic1[0], mic1[1] - 0.05, "M1")
plt.text(mic2[0], mic2[1] - 0.05, "M2")
plt.text(source[0], source[1] + 0.05, "S")

plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.title("Esperimento 1 - Geometria sorgente / microfoni")

plt.axis("equal")
plt.grid()

plt.legend()

plt.show()