# Microphone Array Laboratory

## Panoramica

Questo repository contiene un percorso laboratoriale progressivo dedicato a **microphone arrays, localizzazione acustica, beamforming e acoustic imaging**.

L'obiettivo non è studiare i concetti come argomenti isolati, ma costruire una catena coerente che parta dalla fisica delle onde acustiche e arrivi gradualmente a tecniche avanzate come:

- TDOA e DOA
- FFT e fase
- steering vector
- Delay-and-Sum beamforming
- beam pattern, main lobe, sidelobes e grating lobes
- spatial sampling e spatial aliasing
- near field e far field
- acoustic maps 2D
- Cross-Spectral Matrix (CSM)
- PSD, Welch e coherence
- GCC-PHAT
- sorgenti multiple
- moving-source beamforming
- Doppler
- sorgenti rotanti, BPF e order tracking
- MVDR / Capon
- MUSIC
- eigenvalue decomposition e signal/noise subspaces
- deconvolution
- DAMAS
- CLEAN-SC
- SODIX
- source separation
- monopole, dipole e quadrupole
- propagazione in flusso e Mach number
- uncertainty analysis
- advanced source tracking

Il progetto è pensato come un laboratorio didattico: ogni esperimento introduce pochi concetti nuovi, li collega a quelli precedenti e contiene codice Python eseguibile e modificabile.

---

# Obiettivo generale

Vogliamo arrivare a comprendere e implementare una pipeline completa di acoustic array processing:

```text
fenomeno acustico
      ↓
propagazione
      ↓
microphone array
      ↓
segnali multicanale x_m(t)
      ↓
FFT / STFT
      ↓
relazioni di fase e ritardo
      ↓
TDOA / steering vector
      ↓
CSM
      ↓
beamforming
      ↓
acoustic map
      ↓
source localization
      ↓
tecniche avanzate di separazione e deconvoluzione
```

La domanda centrale è:

> Dati i segnali registrati da più microfoni, come possiamo stimare la direzione, la posizione e le caratteristiche di una o più sorgenti acustiche?

---

# Filosofia del percorso

Il laboratorio segue una progressione pratica.

Ogni esperimento contiene:

1. un obiettivo fisico o numerico;
2. teoria minima necessaria;
3. implementazione Python;
4. grafici;
5. interpretazione dei risultati;
6. piccoli test modificando i parametri.

L'intenzione è evitare blocchi teorici troppo lunghi e mantenere il percorso orientato alla sperimentazione.

---

# Ambiente

Ambiente Python utilizzato:

```text
.venv
```

Esempio di attivazione in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

L'ambiente virtuale viene condiviso tra gli esperimenti del progetto.

Librerie principali utilizzate finora:

```text
numpy
matplotlib
```

Successivamente potranno essere introdotte librerie come `scipy`.

---

# Concetti fondamentali

## Onde acustiche

Relazione fondamentale:

\[
c = f \lambda
\]

dove:

- \(c\) = velocità del suono;
- \(f\) = frequenza;
- \(\lambda\) = lunghezza d'onda.

Con:

\[
c \approx 343 \text{ m/s}
\]

a temperatura ambiente.

La lunghezza d'onda influenza direttamente il comportamento dell'array.

---

## Tempo di propagazione

Per una distanza \(r\):

\[
t = \frac{r}{c}
\]

Questo permette di calcolare il tempo di arrivo del suono a ciascun microfono.

---

## TOA e TDOA

**TOA — Time Of Arrival**

\[
t_m = \frac{r_m}{c}
\]

**TDOA — Time Difference Of Arrival**

\[
\tau_{ij} = t_i - t_j
\]

Il TDOA contiene informazione sulla direzione della sorgente.

---

## Ritardo e fase

Nel dominio della frequenza:

\[
x(t-\tau)
\Longleftrightarrow
X(f)e^{-j2\pi f\tau}
\]

Quindi un ritardo temporale produce una rotazione di fase:

\[
\phi = -2\pi f\tau
\]

Questo collegamento è alla base dello steering vector.

---

# Geometria array utilizzata

La configurazione principale utilizzata negli esperimenti è un **Uniform Linear Array (ULA)**.

Parametri tipici:

```text
M = 8 microfoni
d = 0.05 m
c = 343 m/s
```

Le posizioni dei microfoni sono:

```python
mic_x = (np.arange(M) - (M - 1) / 2) * d
mic_y = np.zeros(M)
```

che per `M = 8` e `d = 0.05 m` produce:

```text
[-0.175
 -0.125
 -0.075
 -0.025
  0.025
  0.075
  0.125
  0.175]
```

L'apertura totale dell'array è:

\[
D = (M-1)d
\]

quindi:

\[
D = 0.35 \text{ m}
\]

---

# Stato attuale

Al momento il percorso è arrivato fino alla costruzione di una **Cross-Spectral Matrix** e al **near-field beamforming 2D con CSM**.

La pipeline implementata attualmente è:

```text
sorgente simulata
      ↓
propagazione verso 8 microfoni
      ↓
segnali temporali multicanale
      ↓
rumore
      ↓
divisione in blocchi
      ↓
window Hann
      ↓
FFT
      ↓
estrazione di un bin di frequenza
      ↓
X(f)
      ↓
X X^H
      ↓
media sui blocchi
      ↓
CSM
      ↓
steering vector near-field
      ↓
P(x,y) = a^H C a
      ↓
acoustic map 2D
      ↓
stima della posizione della sorgente
```

Ultimo risultato verificato:

```text
Posizione reale:   (0.30, 1.00) m
Posizione stimata: (0.30, 0.99875) m
Errore:            circa 1.25 mm
```

Questo risultato proviene da una simulazione ideale, quindi non va interpretato come precisione ottenibile automaticamente su dati reali.

---

# Esperimenti completati

## Esperimento 01 — Tempi di arrivo

Obiettivo:

- introdurre la geometria sorgente-microfono;
- calcolare distanza;
- calcolare TOA;
- calcolare TDOA.

Formula:

\[
t = \frac{r}{c}
\]

e:

\[
TDOA = t_1 - t_2
\]

È stato introdotto anche il limite fisico:

\[
|\tau| \leq \frac{d}{c}
\]

per una coppia di microfoni separati da \(d\).

---

## Esperimento 02 — Segnali campionati e ritardo

Sono stati generati segnali sinusoidali ricevuti da due microfoni.

Concetti introdotti:

- sampling rate;
- periodo di campionamento;
- ritardo espresso in campioni;
- fractional delay;
- relazione tra ritardo temporale e fase.

Formule principali:

\[
T_s = \frac{1}{f_s}
\]

\[
N_{delay} = \tau f_s
\]

\[
\phi = -2\pi f\tau
\]

---

## Esperimento 03 — Rumore e cross-correlation

Sono stati aggiunti:

- rumore;
- segnali broadband;
- cross-correlation;
- stima del TDOA a partire dai dati.

Pipeline:

```text
segnali rumorosi
      ↓
cross-correlation
      ↓
lag del massimo
      ↓
TDOA stimato
```

Formula:

\[
\hat{\tau}
=
\frac{\text{lag del massimo}}{f_s}
\]

Sono stati discussi:

- SNR;
- quantizzazione temporale;
- limiti fisici sul lag;
- ambiguità delle sinusoidi pure.

---

## Esperimento 04 — FFT e fase

Obiettivo:

collegare il ritardo nel dominio del tempo alla fase nel dominio della frequenza.

Sono stati introdotti:

- FFT;
- modulo;
- fase;
- phase wrapping;
- phase ambiguity;
- wavenumber.

Formule:

\[
x(t-\tau)
\Longleftrightarrow
X(f)e^{-j2\pi f\tau}
\]

\[
\Delta\phi = -2\pi f\tau
\]

\[
k = \frac{2\pi f}{c}
\]

---

## Esperimento 05 — Array a 8 microfoni e steering vector

È stato introdotto lo **steering vector**.

Far-field steering:

\[
\tau_m(\theta)
=
\frac{x_m\sin\theta}{c}
\]

\[
a_m(\theta)
=
e^{-j2\pi f\tau_m(\theta)}
\]

Lo steering vector rappresenta la firma teorica di fase che una sorgente proveniente da una certa direzione dovrebbe produrre sui microfoni.

Concettualmente:

```text
direzione ipotizzata
      ↓
ritardi teorici
      ↓
fasi teoriche
      ↓
steering vector
```

---

## Esperimento 06 — Delay-and-Sum Beamforming

È stato implementato il primo beamformer angolare.

Formula:

\[
Y(\theta)
=
a^H(\theta)X
\]

e:

\[
P(\theta)
=
|a^H(\theta)X|^2
\]

Il beamformer prova molti angoli e cerca quello che produce la risposta massima.

È stato introdotto il concetto di DOA:

```text
Direction Of Arrival
```

---

## Esperimento 07 — Beam pattern e risoluzione

Sono stati studiati:

- beam pattern;
- main lobe;
- sidelobes;
- beamwidth;
- Half-Power Beamwidth;
- array aperture;
- risoluzione angolare.

Relazione qualitativa:

\[
\text{beamwidth}
\sim
\frac{\lambda}{D}
\]

Sono stati confrontati:

- diversi numeri di microfoni;
- diverse aperture;
- diverse frequenze.

È stata chiarita la distinzione tra:

```text
M = numero di microfoni
d = spacing
D = apertura
lambda = lunghezza d'onda
```

---

## Esperimento 08 — Spatial aliasing e grating lobes

È stato studiato il campionamento spaziale.

Regola fondamentale:

\[
d \leq \frac{\lambda}{2}
\]

e quindi:

\[
f_{alias}
\approx
\frac{c}{2d}
\]

Sono stati confrontati:

- sidelobes;
- grating lobes;
- aliasing temporale;
- aliasing spaziale.

Concetto centrale:

> Due direzioni differenti possono produrre progressioni di fase indistinguibili quando lo spacing è troppo grande rispetto alla lunghezza d'onda.

---

## Esperimento 09 — Near field, far field e acoustic map 2D

Il laboratorio è passato dal problema:

\[
P(\theta)
\]

al problema:

\[
P(x,y)
\]

Nel near field viene utilizzata la distanza geometrica reale:

\[
r_m(x,y)
=
\sqrt{
(x-x_m)^2+
(y-y_m)^2
}
\]

Steering near-field:

\[
a_m(x,y)
=
e^{-jk(r_m-r_{ref})}
\]

Beamforming:

\[
P(x,y)
=
|a^H(x,y)X|^2
\]

È stata costruita la prima acoustic map 2D.

Sono stati chiariti:

- far field = ricerca principalmente angolare;
- near field = ricerca spaziale;
- onde piane;
- onde sferiche;
- distanza di Fraunhofer.

Una stima comune della distanza di Fraunhofer:

\[
R_F
\approx
\frac{2D^2}{\lambda}
\]

---

## Esperimento 10 — Cross-Spectral Matrix e beamforming CSM

Questo è lo stato attuale del progetto.

L'obiettivo è passare da un singolo vettore complesso \(X\) a una rappresentazione più robusta delle relazioni spettrali dell'array.

Per ogni blocco temporale:

```text
segnale multicanale
      ↓
window
      ↓
FFT
      ↓
X(f)
```

dove:

\[
X(f)
=
\begin{bmatrix}
X_1(f)\\
X_2(f)\\
\vdots\\
X_M(f)
\end{bmatrix}
\]

Viene costruita:

\[
X X^H
\]

e mediata sui blocchi:

\[
\boxed{
C(f)
=
E[X(f)X^H(f)]
}
\]

Questa è la **Cross-Spectral Matrix**.

Per 8 microfoni:

```text
CSM shape = (8, 8)
```

Gli elementi diagonali:

\[
C_{ii}
=
E[|X_i|^2]
\]

rappresentano gli autospectra.

Gli elementi fuori diagonale:

\[
C_{ij}
=
E[X_iX_j^*]
\]

rappresentano i cross-spectra.

Il beamforming diventa:

\[
\boxed{
P(x,y,f)
=
a^H(x,y,f)
C(f)
a(x,y,f)
}
\]

---

# Collegamento tra a^H X e a^H C a

Questo è un punto fondamentale del progetto.

Con un singolo snapshot:

\[
P
=
|a^H X|^2
\]

Sviluppando:

\[
|a^H X|^2
=
(a^H X)(X^H a)
\]

quindi:

\[
|a^H X|^2
=
a^H X X^H a
\]

Se:

\[
C = E[XX^H]
\]

allora:

\[
\boxed{
P
=
a^H C a
}
\]

Quindi \(a^HCa\) non è un algoritmo scollegato dal precedente: è la naturale estensione statistica del beamforming basato su \(a^HX\).

---

# Cosa rappresentano X, a e C

## X

\[
X
\]

rappresenta:

> ciò che i microfoni hanno misurato a una certa frequenza.

Ogni elemento contiene:

- ampiezza;
- fase.

---

## a

\[
a
\]

è lo steering vector:

> ciò che ci aspetteremmo di misurare se la sorgente fosse nella direzione o posizione che stiamo testando.

---

## a^H X

\[
a^H X
\]

misura quanto bene un'ipotesi spaziale combacia con una singola osservazione complessa.

---

## C

\[
C
\]

rappresenta:

> le relazioni spettrali tra tutte le coppie di microfoni.

---

## a^H C a

\[
a^H C a
\]

può essere interpretato come:

> quanta energia della CSM è compatibile con quella posizione o direzione.

---

# Far field e near field: riepilogo

Le due distinzioni principali sono indipendenti.

## Tipo di geometria

### Far field

Steering:

\[
a(\theta)
\]

Ricerca:

```text
theta
```

Output:

\[
P(\theta)
\]

### Near field

Steering:

\[
a(x,y)
\]

Ricerca:

```text
x, y
```

Output:

\[
P(x,y)
\]

---

## Tipo di dati

### Singolo snapshot

\[
|a^HX|^2
\]

### Statistica su più blocchi

\[
a^HCa
\]

Quindi possiamo avere:

| Campo | Dati | Formula |
|---|---|---|
| Far field | singolo snapshot | \(|a^HX|^2\) |
| Far field | CSM | \(a^HCa\) |
| Near field | singolo snapshot | \(|a^HX|^2\) |
| Near field | CSM | \(a^HCa\) |

---

# Risultato attuale dell'Esperimento 10

Parametri:

```text
M = 8
d = 0.05 m
fs = 48000 Hz
f0 = 2000 Hz
source = (0.30, 1.00) m
block_size = 2048
hop_size = 1024
duration = 1 s
```

Bin FFT effettivamente utilizzato:

```text
1992.1875 Hz
```

Questo dipende dalla risoluzione frequenziale:

\[
\Delta f
=
\frac{f_s}{N_{FFT}}
\]

Con:

\[
f_s = 48000
\]

e:

\[
N_{FFT}=2048
\]

si ottiene:

\[
\Delta f = 23.4375\text{ Hz}
\]

La CSM utilizza quindi il bin più vicino a 2000 Hz.

Ultimo output verificato:

```text
Numero blocchi = 45

Shape CSM = (8, 8)

Errore Hermitiano CSM =
2.9103830456733704e-11

Potenza nella posizione reale =
14539323.24463822

Potenza massima della mappa =
14539480.257614734

Posizione reale:
(0.30, 1.00)

Posizione stimata:
(0.30, 0.99875)

Errore di localizzazione:
0.00125 m

NaN presenti = False
Inf presenti = False
Valori negativi = 0
```

Quindi l'Esperimento 10 è attualmente funzionante.

---

# Bug importanti incontrati

## np.zeros

Errore:

```python
beam_map = np.zeros(len(x_scan), len(y_scan))
```

Forma corretta:

```python
beam_map = np.zeros(
    (len(y_scan), len(x_scan))
)
```

---

## Esponenziale complesso

Errore:

```python
np.exp(-1j * k + delta_r)
```

Forma corretta:

```python
np.exp(-1j * k * delta_r)
```

---

## Nome della variabile X

Non usare `x` sia per:

- coordinata spaziale;
- vettore complesso dei microfoni.

Convenzione utilizzata:

```text
x, y    = coordinate
X       = vettore frequenziale
```

---

## Errore nel calcolo della distanza

Errore incontrato:

```python
r_scan = np.sqrt(
    (x - mic_x)** +
    (y - mic_y)**2
)
```

Forma corretta:

```python
r_scan = np.sqrt(
    (x - mic_x)**2
    +
    (y - mic_y)**2
)
```

L'errore generava:

```text
RuntimeWarning: invalid value encountered in power
```

e una falsa localizzazione in:

```text
(-1.0, 0.2)
```

Dopo la correzione la localizzazione è tornata corretta.

---

# Interpretazione dei grafici attuali

## Modulo della CSM

Il grafico:

```python
plt.imshow(np.abs(CSM))
```

mostra:

\[
|C_{ij}|
\]

Gli assi rappresentano coppie di microfoni.

La diagonale rappresenta gli autospectra.

Gli elementi fuori diagonale rappresentano i cross-spectra.

I valori numerici mostrati, ad esempio:

```text
226000
227000
228500
```

non sono direttamente Watt o Pa².

Nell'implementazione attuale sono valori legati alla scala numerica della FFT.

Per ottenere grandezze fisiche correttamente calibrate dovremo introdurre:

- scaling FFT;
- PSD;
- window correction;
- calibrazione microfonica;
- sensibilità dei microfoni.

---

## Acoustic map

La mappa rappresenta:

\[
P(x,y)
\]

Per ogni pixel della griglia il programma costruisce uno steering vector e valuta:

\[
a^H C a
\]

Il massimo rappresenta la posizione più compatibile con la struttura spaziale contenuta nei dati.

Con un ULA la mappa può essere allungata lungo alcune direzioni: non bisogna aspettarsi necessariamente un punto perfettamente circolare.

---

# Prossimo esperimento

## Esperimento 11 — PSD, Welch e Coherence

Il prossimo laboratorio partirà dagli stessi segnali multicanale dell'Esperimento 10.

Obiettivi:

- comprendere meglio la stima spettrale;
- introdurre PSD;
- implementare Welch;
- comprendere autospectrum e cross-spectrum;
- calcolare coherence tra coppie di microfoni.

Argomenti:

\[
PSD
\]

\[
G_{xx}(f)
\]

\[
G_{xy}(f)
\]

e:

\[
\boxed{
\gamma^2_{xy}(f)
=
\frac{|G_{xy}(f)|^2}
{G_{xx}(f)G_{yy}(f)}
}
\]

La coherence sarà interpretata come misura della relazione lineare frequenza-per-frequenza tra due segnali.

---

# Roadmap dei prossimi laboratori

L'ordine potrà essere leggermente adattato durante il percorso, ma la roadmap prevista è la seguente.

---

## Esperimento 11 — PSD, Welch e Coherence

Contenuti:

- periodogram;
- PSD;
- segmentazione;
- overlap;
- Hann window;
- Welch averaging;
- autospectrum;
- cross-spectrum;
- coherence.

Obiettivo:

comprendere come stimare in modo robusto contenuto energetico e relazioni tra microfoni.

---

## Esperimento 12 — GCC-PHAT

Riprendere il problema del TDOA con un metodo più robusto.

Pipeline:

```text
x1(t), x2(t)
      ↓
FFT
      ↓
cross-spectrum
      ↓
PHAT weighting
      ↓
IFFT
      ↓
GCC-PHAT
      ↓
TDOA
```

Formula indicativa:

\[
R_{PHAT}(\tau)
=
\mathcal F^{-1}
\left\{
\frac{X_1X_2^*}
{|X_1X_2^*|}
\right\}
\]

Obiettivo:

confrontare cross-correlation classica e GCC-PHAT.

---

## Esperimento 13 — Due sorgenti

Aggiungere una seconda sorgente.

Studiare:

- due frequenze diverse;
- stessa frequenza;
- sorgenti coerenti;
- sorgenti incoerenti;
- capacità del Delay-and-Sum di separarle.

Obiettivo:

passare da source localization semplice a source separation spaziale.

---

## Esperimento 14 — Risoluzione con due sorgenti

Variare la distanza angolare o spaziale tra due sorgenti.

Studiare:

- limite di risoluzione;
- beamwidth;
- fusione dei main lobes;
- dynamic range;
- influenza di \(M\), \(D\), \(d\), \(f\).

---

## Esperimento 15 — CSM con sorgenti multiple

Costruire la CSM in presenza di due o più sorgenti.

Studiare:

- contributi multipli;
- rank della CSM;
- correlazione tra sorgenti;
- struttura degli autovalori.

Questo sarà il ponte verso MUSIC e metodi subspace.

---

## Esperimento 16 — Eigenvalue decomposition

Decomporre:

\[
C = V\Lambda V^H
\]

Studiare:

- autovalori;
- autovettori;
- rank;
- interpretazione fisica.

Obiettivo:

capire come la struttura della CSM riveli il numero e la struttura delle sorgenti.

---

## Esperimento 17 — Signal e Noise Subspaces

Separare:

```text
signal subspace
noise subspace
```

Analizzare come cambiano al variare di:

- numero di sorgenti;
- rumore;
- SNR;
- numero di microfoni.

Preparazione diretta a MUSIC.

---

## Esperimento 18 — MUSIC

Implementare MUSIC.

Pseudospectrum:

\[
P_{MUSIC}(\theta)
=
\frac{1}
{a^H E_nE_n^Ha}
\]

Studiare:

- maggiore risoluzione rispetto al Delay-and-Sum;
- dipendenza dalla stima del numero di sorgenti;
- sensibilità al modello;
- sorgenti coerenti.

---

## Esperimento 19 — MVDR / Capon

Implementare:

\[
w_{MVDR}
=
\frac{C^{-1}a}
{a^HC^{-1}a}
\]

e/o lo spectrum:

\[
P_{MVDR}
=
\frac{1}
{a^HC^{-1}a}
\]

Confrontare:

```text
Delay-and-Sum
vs
MVDR
vs
MUSIC
```

in termini di:

- risoluzione;
- sidelobes;
- rumore;
- robustezza.

---

## Esperimento 20 — Deconvolution e PSF

Introdurre la Point Spread Function.

Concetto:

```text
sorgente ideale
      ↓
risposta dell'array
      ↓
PSF
```

Interpretare la beamforming map come:

\[
\text{Map}
\approx
\text{Sources} * \text{PSF}
\]

Obiettivo:

comprendere perché il beamforming classico produce sorgenti "sfocate".

---

## Esperimento 21 — DAMAS

Implementare o studiare DAMAS.

Obiettivo:

deconvolvere la mappa acustica e stimare distribuzioni di sorgenti più concentrate.

Studiare:

- matrice PSF;
- iterative solution;
- convergenza;
- source power.

---

## Esperimento 22 — CLEAN-SC

Studiare CLEAN-SC.

Obiettivo:

ridurre sidelobes e separare sorgenti dominanti sfruttando la struttura di coerenza.

Confronto previsto:

```text
Conventional Beamforming
DAMAS
CLEAN-SC
```

---

## Esperimento 23 — SODIX

Introduzione a SODIX e ai metodi di fitting distribuito.

Obiettivo:

comprendere un approccio più avanzato alla stima quantitativa delle sorgenti.

---

# Blocco sorgenti mobili

Dopo aver consolidato il beamforming statico, il progetto passerà alle sorgenti mobili.

---

## Esperimento 24 — Sorgente in movimento

Definire una traiettoria:

\[
\mathbf r_s(t)
\]

Studiare:

- distanze variabili;
- ritardi variabili;
- steering vector tempo-dipendente;
- acoustic map nel tempo.

---

## Esperimento 25 — Doppler

Studiare il cambiamento di frequenza dovuto al moto relativo.

Concetti:

- approaching source;
- receding source;
- Doppler shift;
- spettrogramma.

Obiettivo:

visualizzare la frequenza osservata come funzione del tempo.

---

## Esperimento 26 — Moving-Source Beamforming

Usare una traiettoria nota o stimata.

Studiare:

- compensazione del movimento;
- steering dinamico;
- time-domain moving-source beamforming;
- frequenze Doppler-shifted.

Questo blocco è direttamente collegato all'interesse per l'analisi di phased array data per moving sources.

---

# Blocco sorgenti rotanti

## Esperimento 27 — Rotating Source

Simulare una sorgente rotante o un rotore.

Parametri:

- RPM;
- numero di pale;
- raggio;
- velocità angolare.

---

## Esperimento 28 — Blade Passing Frequency

Definire:

\[
f_{rot}
=
\frac{RPM}{60}
\]

e:

\[
\boxed{
BPF
=
N_b f_{rot}
}
\]

Studiare:

- BPF;
- armoniche;
- tonal noise.

---

## Esperimento 29 — Order Tracking

Definire:

\[
Order
=
\frac{f}{f_{rot}}
\]

Studiare:

- 1X;
- 2X;
- blade orders;
- frequenze che cambiano con RPM.

---

# Blocco aeroacustica

## Esperimento 30 — Tonal e Broadband Noise

Separare concettualmente:

```text
tonal noise
broadband noise
```

Analizzare esempi di:

- rotori;
- ventole;
- flussi turbolenti.

---

## Esperimento 31 — Monopole, Dipole, Quadrupole

Studiare i tre modelli fondamentali di sorgente acustica.

### Monopole

Variazione di volume.

### Dipole

Forza oscillante.

### Quadrupole

Fluttuazioni associate allo stress del flusso.

Obiettivo:

collegare source models e aeroacustica.

---

## Esperimento 32 — Propagation in Flow

Introdurre velocità del flusso:

\[
U
\]

e Mach number:

\[
\boxed{
Ma
=
\frac{U}{c}
}
\]

Studiare come il flusso modifichi:

- propagazione;
- tempi di arrivo;
- steering;
- beamforming.

---

# Blocco realistico / sperimentale

## Esperimento 33 — Microphone Characteristics

Studiare:

- sensitivity;
- frequency response;
- phase response;
- self-noise;
- dynamic range;
- clipping;
- directivity.

---

## Esperimento 34 — Calibration

Introdurre la calibrazione.

Passaggio da:

```text
ADC units
```

a grandezze fisiche, ad esempio:

```text
Pa
Pa²
Pa²/Hz
dB SPL
```

Questo permetterà di interpretare fisicamente PSD e CSM.

---

## Esperimento 35 — Uncertainty Analysis

Analizzare la sensibilità della localizzazione a:

- posizione microfoni;
- velocità del suono;
- rumore;
- frequenza;
- sampling rate;
- dimensione griglia;
- calibrazione;
- errori di fase.

Obiettivo:

distinguere precisione numerica da accuratezza fisica.

---

## Esperimento 36 — Advanced Source Tracking

Combinare:

- acoustic maps nel tempo;
- peak detection;
- trajectory estimation;
- moving-source beamforming;
- uncertainty.

Possibili estensioni:

- Kalman filtering;
- multi-source tracking;
- trajectory smoothing.

---

# Source Separation

Il tema della source separation attraverserà più esperimenti.

Approcci previsti:

- separazione spaziale tramite beamforming;
- sorgenti multiple;
- MVDR;
- MUSIC;
- masking tempo-frequenza;
- eventualmente tecniche più avanzate in un modulo dedicato.

L'obiettivo non sarà solo dire:

```text
"dove si trova la sorgente?"
```

ma arrivare anche a:

```text
"quale parte del segnale appartiene a ciascuna sorgente?"
```

---

# Obiettivo finale del progetto

Alla fine del percorso vogliamo essere in grado di:

1. descrivere la propagazione acustica verso un array;
2. progettare una geometria microfonica;
3. riconoscere spatial aliasing e grating lobes;
4. lavorare nel dominio del tempo e della frequenza;
5. stimare TDOA e DOA;
6. costruire steering vectors;
7. costruire una CSM;
8. generare acoustic maps;
9. localizzare sorgenti near-field e far-field;
10. analizzare sorgenti multiple;
11. confrontare Delay-and-Sum, MVDR e MUSIC;
12. comprendere la PSF;
13. applicare tecniche di deconvolution;
14. analizzare sorgenti mobili;
15. comprendere Doppler;
16. analizzare sorgenti rotanti;
17. identificare BPF e ordini;
18. collegare il tutto ad applicazioni aeroacustiche;
19. calibrare una catena di misura;
20. valutare incertezza e limiti del sistema.

---

# Mappa concettuale completa

```text
ONDE ACUSTICHE
      ↓
c = f lambda
      ↓
propagazione
      ↓
TOA
      ↓
TDOA
      ↓
campionamento
      ↓
FFT
      ↓
fase
      ↓
array geometry
      ↓
spatial sampling
      ↓
steering vector
      ↓
Delay-and-Sum
      ↓
beam pattern
      ↓
main lobe / sidelobes
      ↓
array aperture
      ↓
spatial resolution
      ↓
grating lobes / aliasing
      ↓
far field / near field
      ↓
acoustic map
      ↓
CSM
      ↓
PSD / Welch / coherence
      ↓
GCC-PHAT
      ↓
multiple sources
      ↓
eigenvalue decomposition
      ↓
signal/noise subspaces
      ↓
MUSIC / MVDR
      ↓
PSF
      ↓
DAMAS / CLEAN-SC / SODIX
      ↓
moving sources
      ↓
Doppler
      ↓
moving-source beamforming
      ↓
rotating sources
      ↓
BPF / order tracking
      ↓
monopole / dipole / quadrupole
      ↓
propagation in flow
      ↓
Mach number
      ↓
calibration
      ↓
uncertainty analysis
      ↓
advanced source tracking
```

---

# Nota per una nuova chat

Se questo README viene fornito a una nuova conversazione, il punto di ripartenza consigliato è:

> Il progetto ha completato gli esperimenti 01–10. L'ultimo esperimento funzionante costruisce una CSM da segnali simulati di 8 microfoni e utilizza near-field Delay-and-Sum nella forma \(P=a^HCa\) per localizzare una sorgente 2D. Il risultato attuale localizza correttamente una sorgente reale in `(0.30, 1.00)` m con stima `(0.30, 0.99875)` m. Il prossimo laboratorio previsto è Esperimento 11: PSD, Welch e coherence.

Prima di introdurre nuovi algoritmi, è utile mantenere coerenti queste convenzioni:

```text
X       = vettore complesso misurato sui microfoni
a       = steering vector
C / CSM = Cross-Spectral Matrix
x, y    = coordinate spaziali
M       = numero microfoni
d       = spacing
D       = aperture
f0      = frequenza sorgente nominale
f_bin   = frequenza reale del bin FFT utilizzato
k       = 2*pi*f_bin/c
```

Per il near field:

\[
r_m
=
\sqrt{
(x-x_m)^2+
(y-y_m)^2
}
\]

\[
\Delta r_m
=
r_m-r_{ref}
\]

\[
a_m
=
e^{-jk\Delta r_m}
\]

e il beamforming attuale usa:

\[
\boxed{
P(x,y)
=
a^H C a
}
\]

---

# Stato del progetto

```text
[COMPLETATO] Esperimenti 01–10
[PROSSIMO]   Esperimento 11 — PSD / Welch / Coherence
[PIANIFICATO] GCC-PHAT
[PIANIFICATO] Multi-source localization
[PIANIFICATO] Eigenvalue decomposition
[PIANIFICATO] MUSIC
[PIANIFICATO] MVDR / Capon
[PIANIFICATO] PSF / Deconvolution
[PIANIFICATO] DAMAS / CLEAN-SC / SODIX
[PIANIFICATO] Moving sources
[PIANIFICATO] Doppler
[PIANIFICATO] Rotating sources / BPF / Order Tracking
[PIANIFICATO] Aeroacoustics
[PIANIFICATO] Calibration
[PIANIFICATO] Uncertainty analysis
[PIANIFICATO] Advanced source tracking
```

---

## Stato attuale in una frase

> Il progetto ha costruito, passo dopo passo, le basi fisiche e numeriche del microphone-array processing ed è arrivato a una pipeline funzionante di **near-field acoustic imaging basata su CSM e Delay-and-Sum**; il prossimo blocco consoliderà l'analisi spettrale con **PSD, Welch e coherence**, prima di passare a sorgenti multiple e beamforming avanzato.
