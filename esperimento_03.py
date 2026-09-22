# CALCULATION OF TDOA USING CROSS-CORRELATION

# CROSS CORRELATION: tende a rafforzare ciò che è comune/coerente tra i microfoni e a rendere meno importante ciò che non lo è 

import numpy as np
import matplotlib.pyplot as plt

# PARAMETRI
c = 343.0 # m/s velocità della luce
fs = 48000
duration = 0.05

mic1 = np.array([-0.1, 0.0])
mic2 = np.array([0.1, 0.0])

source = np.array([0.6, 1.0])

# GEOMETRIA
r1 = np.linalg.norm(source - mic1)
r2 = np.linalg.norm(source - mic2)

t1 = r1/c
t2 = r2/c

true_tdoa = t1 - t2

print("TDOA teorico:")
print(true_tdoa * 1e6, "microsecondi")

print("TDOA teorico in campioni:", true_tdoa * fs)

# SEGNALE DELLA SORGENTE
N = int(duration * fs)
rng = np.random.default_rng(42) # Random Number Generator con seed 42
source_signal = rng.normal(0, 1, N) # Creazione N numeri casuali distribuiti secondo una distribuzione normale (Gaussiana) dove 0 = media, 1 = deviazione standard e N numero di campioni

# RITARDI DIGITALI 
# Quindi il concetto è questo:
# Calcoliamo il ritardo in campioni quindi quanti campioni passano dal momento in cui la sorgente emette al momento in cui arriva al mic 1 e mic2
# Dopo di che calcolo il tempo totale cioè N quindi i campioni per la durata totale e poi ci sommo il massimo tra i due ritardi in modo che dopo possiamo avere un array
# in cui i primi valori sono 0 fino al valore del delay e poi il resto è il segnale che ha durata N

delay1 = round(t1 * fs)
delay2 = round(t2 * fs)

print()
print("Delay mic1:", delay1, "campioni")
print("Delay mic2:", delay2, "campioni")

total_length = N + max(delay1, delay2)

signal1 = np.zeros(total_length)
signal2 = np.zeros(total_length)

signal1[delay1:delay1 + N] = source_signal
signal2[delay2:delay2 + N] = source_signal

# AGGIUNGIAMO RUMORE
noise_level = 0.5

noise1 = rng.normal(0, noise_level, total_length)
noise2 = rng.normal(0, noise_level, total_length)

signal1_noisy = signal1 + noise1
signal2_noisy = signal2 + noise2

# CROSS CORRELATION
# prova diversi spostamenti temporali tra i due segnali e per ogni spostamento calcola quanto si somigliano
# R12[k] = sommatoriaN x1[n]x2[n-k] dove k è il lag quindi di quanti campioni stiamo spostando un segnale rispetto all'altro

correlation = np.correlate(signal1_noisy, signal2_noisy, mode="full") # mode = full prova tutti gli spostamenti possibili tra i due segnali (N1 + N2 - 1)
lags = np.arange(-len(signal2_noisy) + 1, len(signal1_noisy)) # costruisce l'array contenente lo spostamento in campioni associato a ogni valore di correlazione

# posizione del massimo

peak_index = np.argmax(correlation) # restituisce la posizione del valore massimo nell'array

estimated_lag = lags[peak_index]

estimated_tdoa = estimated_lag / fs # convertiamo il ritardo espresso in campioni in un ritardo espresso in secondi

# quindi gli step sono questi:
# 1) Prova a spostare i due segnali tra loro e misura quanto si assomigliano
# 2) crea l'elenco degli spostamenti possibili, espressi in campioni
# 3) trova dove la somiglianza è massima
# 4) scopre a quanti campioni di ritardo corrisponde quel massimo
# 5) trasforma il ritardo da campioni a secondi 

print()
print("Lag stimato:", estimated_lag, "campioni")

print(
    "TDOA stimato:",
    estimated_tdoa * 1e6,
    "microsecondi"
)

# UN ALTRO MODO GESTENDOLO IN MODO DA VERIFICARE LA CORRETTEZZA DEI VALIRI DEI LAGs
max_lag = int(np.ceil((0.2 / c) * fs))
valid = np.abs(lags) <= max_lag

correlation_valid = correlation[valid]
lags_valid = lags[valid]

peak_index = np.argmax(correlation_valid)

estimated_lag = lags_valid[peak_index]

estimated_tdoa = estimated_lag / fs

# Errore di Stima
error = estimated_tdoa - true_tdoa

print(
    "Errore:",
    error * 1e6,
    "microsecondi"
)

# ==========================================
# GRAFICO CROSS-CORRELATION
# ==========================================

lags_ms = lags / fs * 1000

plt.figure(figsize=(10, 5))

plt.plot(
    lags_ms,
    correlation
)

plt.axvline(
    estimated_tdoa * 1000,
    linestyle="--",
    label="TDOA stimato"
)

plt.xlabel("Lag [ms]")
plt.ylabel("Cross-correlation")

plt.title(
    "Cross-correlation tra Mic 1 e Mic 2"
)

plt.grid()
plt.legend()

plt.xlim(-1, 1)

plt.show()