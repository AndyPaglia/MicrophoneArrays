# MovingSourceArrayLab

## Obiettivo del progetto

`MovingSourceArrayLab` è un laboratorio Python progressivo dedicato all’analisi di dati da microphone array per localizzazione acustica, sound source mapping, Point Spread Function (PSF), deconvoluzione e, in seguito, sorgenti in movimento con effetto Doppler.

L’obiettivo finale è arrivare a una pipeline semplificata ma completa del tipo:

microphone signals  
→ beamforming  
→ sound source map  
→ PSF  
→ deconvolution  
→ stima quantitativa delle sorgenti  
→ moving source  
→ Doppler  
→ trajectory-aware beamforming

Il progetto è pensato come laboratorio didattico: ogni esercizio introduce pochi concetti nuovi, con formule, simulazioni e grafici.

---

## Struttura del progetto

Questo laboratorio è parallelo al progetto già esistente `MicrophoneArray`, ma usa lo stesso ambiente Python e lo stesso `requirements.txt`.

Naming convention:

```text
MovingSourceArrayLab_esperimento_01.py
MovingSourceArrayLab_esperimento_02.py
MovingSourceArrayLab_esperimento_03.py
...
```

L’ambiente virtuale è lo stesso:

```text
.venv
```

Librerie principali:

```text
numpy
matplotlib
scipy
```

---

# Stato attuale del laboratorio

Siamo arrivati a:

```text
MovingSourceArrayLab_esperimento_05.py
```

Gli esperimenti precedenti sono già stati svolti e compresi.

---

# Esperimento 01

## Linear Microphone Array + Point Source

Obiettivo:

- creare un array lineare di microfoni;
- definire una sorgente puntiforme;
- calcolare la distanza sorgente-microfono;
- calcolare i tempi di propagazione;
- calcolare i ritardi relativi tra i microfoni.

Array corrente:

```python
M = 8
d = 0.05
```

Posizioni microfoni:

```python
mic_x = (np.arange(M) - (M - 1)/2) * d
mic_y = np.zeros(M)
```

Sorgente tipica:

```python
source_x = 0.30
source_y = 1.00
```

Distanza:

\[
r_m =
\sqrt{
(x_s-x_m)^2 +
(y_s-y_m)^2
}
\]

Tempo di propagazione:

\[
t_m = \frac{r_m}{c}
\]

Ritardo relativo:

\[
\tau_m =
t_m - \min(t_m)
\]

Concetto principale:

geometria  
→ distanza  
→ tempo di propagazione  
→ ritardo relativo

---

# Esperimento 02

## Simulazione dei segnali ai microfoni

Obiettivo:

simulare ciò che ogni microfono riceve.

Con una sorgente sinusoidale:

\[
s(t)=\sin(2\pi f_0t)
\]

il microfono m riceve:

\[
x_m(t)=
\sin\left(
2\pi f_0(t-\tau_m)
\right)
\]

Il segnale è quindi lo stesso, ma ritardato.

Importante:

\[
s(t-\tau)
\]

significa ritardo temporale.

La matrice:

```python
mic_signals
```

ha forma:

```text
M x N
```

dove:

- righe = microfoni;
- colonne = campioni temporali.

---

# Esperimento 03

## First 2D Time-Domain Beamforming Map

Qui viene costruita la prima vera sound source map.

Viene definita una griglia:

```python
x_scan = np.linspace(-1.0, 1.0, 81)
y_scan = np.linspace(0.2, 2.0, 81)
```

Questi limiti NON sono vincoli fisici.

Definiscono semplicemente l’area in cui vogliamo cercare la sorgente.

Per ogni punto della griglia:

1. si ipotizza che la sorgente sia lì;
2. si calcolano le distanze attese verso i microfoni;
3. si calcolano i ritardi attesi;
4. si convertono in campioni;
5. si riallineano i segnali reali;
6. si sommano;
7. si calcola la potenza.

Principio:

```text
posizione corretta
→ ritardi corretti
→ segnali allineati
→ somma coerente
→ potenza alta
```

Il massimo della beam map fornisce la posizione stimata.

Risultato ottenuto:

```text
True source:
0.3 1.0

Estimated source:
0.30000000000000004 0.9875
```

Quindi il beamformer ha localizzato correttamente la sorgente.

Limite importante dell’Esperimento 03:

i ritardi venivano arrotondati a campioni interi con:

```python
np.round(scan_delays * fs)
```

Quindi, ad esempio:

```text
3.62 campioni
```

diventavano:

```text
4 campioni
```

---

# Esperimento 04

## Prima esplorazione della Point Spread Function

Obiettivo:

capire come una sorgente puntiforme viene rappresentata dal microphone array.

Una sorgente reale puntiforme non appare necessariamente come un punto perfetto nella beam map.

La risposta dell’array contiene:

- main lobe;
- spreading spaziale;
- sidelobes;
- possibili ambiguità.

Questa risposta è legata alla:

```text
Point Spread Function (PSF)
```

La mappa è stata normalizzata:

```python
psf = beam_map / np.max(beam_map)
```

in modo che:

```text
PSF massimo = 1
```

---

## Problema scoperto nell’Esperimento 04

Con una sorgente sinusoidale pura a:

```python
f0 = 2000
```

la PSF risultava molto larga e ambigua.

Motivo principale:

una sinusoide è periodica.

Per:

\[
f_0=2000\,Hz
\]

il periodo è:

\[
T=\frac{1}{f_0}=0.5\,ms
\]

Con:

```text
fs = 48000 Hz
```

un periodo corrisponde a:

```text
24 campioni
```

Quindi ritardi differenti di un intero periodo possono produrre fasi molto simili.

Questo genera ambiguità spaziali e mappe con strutture poco pulite.

Lezione importante:

trovare il massimo nella posizione corretta NON significa necessariamente avere una buona source map.

---

# Esperimento 05 - STATO ATTUALE

## Broadband Source + Fractional Delay Beamforming

Questo è l’esperimento da cui bisogna riprendere.

L’obiettivo è migliorare il beamforming rispetto agli esperimenti precedenti introducendo:

```text
1. segnale broadband
2. fractional delays
```

---

## Segnale broadband

Invece di una sola sinusoide si usa rumore filtrato.

Esempio:

```python
rng = np.random.default_rng(42)

white_noise = rng.standard_normal(N)
```

Filtro band-pass:

```python
from scipy.signal import butter, sosfiltfilt

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
```

Il segnale contiene quindi molte frequenze.

Questo aiuta perché un ritardo errato può magari allineare una frequenza, ma difficilmente allinea correttamente tutto il segnale broadband.

Quindi:

```text
ritardo corretto
→ molte frequenze allineate
→ forte correlazione
→ beamformer power alta
```

---

## Fractional delays

Ora non vogliamo più limitare i ritardi a numeri interi di campioni.

Esempio:

```text
3.62 campioni
```

deve rimanere circa:

```text
3.62
```

e non diventare:

```text
4
```

Per simulare il segnale ritardato si usa:

```python
delayed_time = t - tau

mic_signals[m] = np.interp(
    delayed_time,
    t,
    source_signal,
    left=0,
    right=0
)
```

Questo implementa:

\[
x_m(t)=s(t-\tau_m)
\]

anche per ritardi frazionari.

Durante il beamforming si fa l’operazione inversa:

```python
shifted_time = t + tau
```

per cercare di compensare il ritardo.

Infatti:

\[
x_m(t+\tau_m)
=
s(t)
\]

se il ritardo ipotizzato è corretto.

---

# Parametri attuali

Usare:

```python
c = 343.0
fs = 48000
duration = 0.05

M = 8
d = 0.05

source_x = 0.30
source_y = 1.00
```

ATTENZIONE:

`d` deve essere:

```python
d = 0.05
```

e NON:

```python
d = 0.5
```

---

# Spatial resolution

La risoluzione spaziale dipende principalmente da:

- lunghezza d’onda;
- apertura dell’array;
- numero e posizione dei microfoni;
- distanza della sorgente;
- algoritmo di beamforming.

Relazione utile:

\[
\Delta\theta
\sim
\frac{\lambda}{D}
\]

con:

\[
\lambda=\frac{c}{f}
\]

e:

\[
D=(M-1)d
\]

Quindi:

```text
array più grande
→ main lobe più stretto
→ migliore risoluzione angolare
```

---

# Spatial aliasing

Per un array lineare uniforme è importante ricordare:

\[
d\leq\frac{\lambda}{2}
\]

Per:

```text
d = 0.05 m
```

la frequenza approssimativa oltre la quale può comparire spatial aliasing è:

\[
f_{max}
\approx
\frac{c}{2d}
\]

\[
f_{max}
\approx3430\,Hz
\]

Quindi il filtro attuale:

```text
500 - 4000 Hz
```

supera leggermente questa soglia.

Questo potrà essere studiato esplicitamente in un laboratorio futuro.

---

# Roadmap futura

## Esperimento 06
### Quantitative PSF Analysis

Obiettivi:

- ottenere una PSF con il nuovo beamformer broadband;
- studiare main lobe e sidelobes;
- estrarre sezioni orizzontali e verticali;
- misurare la larghezza della PSF;
- introdurre FWHM.

---

## Esperimento 07
### Frequency and Array Aperture

Studiare come cambiano risoluzione e PSF variando:

```text
frequenza
numero di microfoni
apertura D
```

Confronti previsti:

```text
M = 8
M = 16
```

---

## Esperimento 08
### Spatial Aliasing

Variare:

```text
d
```

e osservare:

- sidelobes;
- grating lobes;
- ambiguità spaziali.

---

## Esperimento 09
### Two Sources

Simulare due sorgenti puntiformi indipendenti.

Obiettivo:

capire quando due sorgenti vicine possono essere distinte.

---

## Esperimento 10
### Dynamic Range

Simulare:

```text
sorgente forte
+
sorgente debole
```

e osservare quando la sorgente debole viene nascosta dai sidelobes della sorgente forte.

---

## Esperimento 11
### Deconvolution Model

Introduzione al modello:

\[
B(x,y)
\approx
S(x,y)*PSF(x,y)
\]

dove:

```text
S = sorgenti reali
PSF = risposta dell’array
B = beamforming map
```

---

## Esperimento 12
### First Deconvolution

Implementare un primo algoritmo di deconvoluzione.

Possibili metodi:

```text
Richardson-Lucy
CLEAN-like
```

Confrontare:

```text
beamforming map
vs
deconvolved map
```

---

## Esperimento 13
### Multiple Sources + Deconvolution

Studiare la separazione di sorgenti vicine dopo la deconvoluzione.

---

## Esperimento 14
### Acoustic Power Integration

Integrare la potenza su regioni diverse della mappa:

\[
P_R
=
\int_R P(x,y)dA
\]

Obiettivo:

ottenere un ranking quantitativo delle sorgenti.

---

# Moving Sources

Solo dopo aver completato bene il caso statico si passa alle sorgenti in movimento.

---

## Esperimento 15
### Known Source Trajectory

Definire una sorgente che si muove:

\[
x_s(t)=x_0+vt
\]

e quindi:

\[
\tau_m=\tau_m(t)
\]

---

## Esperimento 16
### Time-Varying Delays

Simulare segnali microfonici con ritardi che cambiano continuamente nel tempo.

---

## Esperimento 17
### Doppler Effect

Studiare come il moto della sorgente produce Doppler.

Il segnale ricevuto diventa:

\[
x_m(t)
=
s(t-\tau_m(t))
\]

---

## Esperimento 18
### Source Signal Reconstruction

Usando la traiettoria nota, tentare di ricostruire il segnale nel sistema di riferimento della sorgente.

---

## Esperimento 19
### Moving-Source Beamforming

Applicare time-domain beamforming con ritardi dipendenti dal tempo.

---

## Esperimento 20
### Moving-Source PSF

Studiare come la PSF cambia per una sorgente in movimento.

---

## Esperimento 21
### Moving-Source Deconvolution

Applicare la deconvoluzione alle mappe di sorgenti in movimento.

---

# Progetto finale

Simulare un flyover semplificato.

Scenario:

```text
             sorgente/aereo in movimento

        → → → → → → → → → →

                 ↓

---------------------------------------

●   ●   ●   ●   ●   ●   ●   ●
microphone array
```

Obiettivi finali:

- traiettoria nota;
- sorgenti multiple;
- Doppler;
- fractional delays;
- beamforming;
- source maps;
- PSF;
- deconvolution;
- integrazione della potenza;
- ranking delle sorgenti acustiche.

---

# Punto da cui riprendere

Se questo README viene passato a una nuova chat, il progetto deve riprendere da:

```text
MovingSourceArrayLab_esperimento_05.py
```

Lo stato attuale è:

```text
broadband source
+
fractional delay interpolation
+
time-domain delay-and-sum beamforming
```

Il prossimo passo NON è ancora la deconvoluzione.

Prima bisogna:

```text
validare Esperimento 05
→ analizzare bene la beam map
→ costruire una PSF quantitativa
→ misurare risoluzione e sidelobes
→ introdurre due sorgenti
→ studiare dynamic range
→ poi passare alla deconvoluzione
```

Obiettivo didattico generale:

non usare gli algoritmi come black box.

Ogni fase deve essere capita in termini di:

```text
fisica
→ formula
→ codice
→ grafico
→ interpretazione
→ limite
→ miglioramento successivo
```
