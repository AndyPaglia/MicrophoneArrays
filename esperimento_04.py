# 4) FFT AND PHASE DIFFERENCE 

# x1(t), x2(t)
# x2(t) = x1(t-tau)
# x(t-tau) = X(f)*e^(-j*2*pi*f*tau) --> un ritardo nel tempo diventa una rotazione di fase nel dominio delle frequenze

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI
c = 343.0 # m/s velocità della luce
fs = 48000
duration = 0.05
f0 = 500.0

mic1 = np.array([-0.1, 0.0])
mic2 = np.array([0.1, 0.0])

source = np.array([0.6, 1.0])

# GEOMETRIA

r1 = np.linalg.norm(source - mic1)
r2 = np.linalg.norm(source - mic2)

t1 = r1 / c
t2 = r2 / c

tdoa = t1 - t2

print("r1 =", r1, "m")
print("r2 =", r2, "m")

print("t1 =", t1 * 1e3, "ms")
print("t2 =", t2 * 1e3, "ms")

print("TDOA =", tdoa * 1e6, "microsecondi")

# ASSE TEMPORALE

N = int(duration * fs) # Durata temporale in numero di campioni

t = np.arange(N) / fs # 1/fs è la durata di un singolo campione. Trova il tempo ad ogni campione che passa quindi dice a quale istante temporale corrisponde ciascuno di quei 2400 campioni

# SEGNALI AI MICROFONI

signal1 = np.sin(2 * np.pi * f0 * (t - t1))

signal2 = np.sin(2 * np.pi * f0 * (t - t2))

# FFT

X1 = np.fft.rfft(signal1) # rfft significa che i due segnali sono segnali reali. Restituisce da 0 a fs/2 perchè da -fs/2 a 0 sarebbe ridondante 
X2 = np.fft.rfft(signal2)

freqs = np.fft.rfftfreq(N, d=1/fs)

# TROVIAMO IL BIN PIU VICINO A f0

index_f0 = np.argmin(
    np.abs(freqs - f0)
)

f_bin = freqs[index_f0]

print()
print("Frequenza FFT più vicina =", f_bin, "Hz")

# MODULO E FASE

amp1 = np.abs(X1[index_f0])
amp2 = np.abs(X2[index_f0])

phase1 = np.angle(X1[index_f0])
phase2 = np.angle(X2[index_f0])

phase_diff = phase1 - phase2

# portiamo la fase tra -pi e pi
phase_diff_wrapped = np.angle(
    np.exp(1j * phase_diff)
)

print()
print("Ampiezza Mic1 =", amp1)
print("Ampiezza Mic2 =", amp2)

print()
print("Fase Mic1 =", phase1, "rad")
print("Fase Mic2 =", phase2, "rad")

print()
print(
    "Differenza di fase FFT =",
    phase_diff_wrapped,
    "rad"
)

print(
    "Differenza di fase FFT =",
    np.degrees(phase_diff_wrapped),
    "gradi"
)

# FASE TEORICA

phase_theoretical = -2 * np.pi * f0 * tdoa

phase_theoretical_wrapped = np.angle(
    np.exp(1j * phase_theoretical)
)

print()
print(
    "Differenza di fase teorica =",
    phase_theoretical_wrapped,
    "rad"
)

print(
    "Differenza di fase teorica =",
    np.degrees(phase_theoretical_wrapped),
    "gradi"
)

# GRAFICO FFT

plt.figure(figsize=(10, 5))

plt.plot(
    freqs,
    np.abs(X1),
    label="Mic 1"
)

plt.plot(
    freqs,
    np.abs(X2),
    label="Mic 2",
    alpha=0.8
)

plt.xlim(0, 3000)

plt.xlabel("Frequenza [Hz]")
plt.ylabel("|X(f)|")

plt.title("FFT dei due segnali")

plt.grid()
plt.legend()

plt.show()

# Grafico Fase

plt.figure(figsize=(7, 5))

plt.scatter(
    [1, 2],
    [
        np.degrees(phase1),
        np.degrees(phase2)
    ]
)

plt.xticks(
    [1, 2],
    ["Mic 1", "Mic 2"]
)

plt.ylabel("Fase [gradi]")

plt.title(
    f"Fase a {f_bin:.1f} Hz"
)

plt.grid()

plt.show()
