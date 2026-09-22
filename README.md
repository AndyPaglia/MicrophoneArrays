# Microphone Array Laboratory

Personal laboratory of Python experiments for studying **acoustic signal processing, microphone arrays, source localization and beamforming**.

The repository follows a progressive learning path, starting from basic sound propagation and gradually introducing spatial audio processing techniques.

## Experiments

- **Experiment 01 — TOA & TDOA**  
  Source-microphone geometry, propagation time and Time Difference of Arrival.

- **Experiment 02 — Acoustic Delay**  
  Simulation of a sinusoidal source received by two microphones and observation of propagation delays.

- **Experiment 03 — Cross-Correlation**  
  Estimation of TDOA from microphone signals using cross-correlation, including noisy signals.

- **Experiment 04 — FFT & Phase**  
  Frequency-domain analysis and relationship between time delay and phase difference:
  
  \[
  \Delta\phi = -2\pi f\tau
  \]

- **Experiment 05 — Microphone Array & Steering Vector**  
  Extension to an 8-microphone linear array and study of the phase pattern produced by different source directions.

- **Experiment 06 — Delay-and-Sum Beamforming**  
  Direction-of-Arrival estimation by scanning different angles and coherently combining microphone signals.

- **Experiment 07 — Beam Pattern** 
  Main lobe, sidelobes, angular resolution and array geometry.

## Learning path

```text
Sound propagation
      ↓
TOA / TDOA
      ↓
Cross-correlation
      ↓
FFT & Phase
      ↓
Microphone Arrays
      ↓
Steering Vector
      ↓
Delay-and-Sum Beamforming
      ↓
Beam Pattern & Source Localization
```

The main idea explored throughout the experiments is:

**Direction → Path difference → Time delay → Phase difference → Spatial processing**

## Tools

- Python
- NumPy
- Matplotlib

## Status

Work in progress. New experiments will be added.
