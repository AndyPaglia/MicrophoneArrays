# 01) LINEAR MICROPHONE ARRAY + PUNTIFORM SOURCE 
# Analyze source-microphone distance and the propagation time

import numpy as np
import matplotlib.pyplot as plt

# FIXED PARAMETERS
c = 343 # m/s - sound velocity

# MICROPHONE ARRAY
M = 8 # Number of microphones
d = 0.05 # Distance between a mic and another in meters

# Mic position centered in zero
mic_x = (np.arange(M) - (M - 1)/2) * d
# Starting from -0.175 to +0.175
mic_y = np.zeros(M)

# SOURCE POSITION
source_x = 0.30 # meters
source_y = 1.00 # meters

# Calculate the distances between source and microphones
distances = np.sqrt((source_x - mic_x)**2 + (source_y - mic_y)**2)
# we obtain a distance for each mic

# Since now we have the "s" term so the position, we want to find the time that passed from the moment the source started to emit to the time the microphone received that pressure
arrival_times = distances/c # absolute propagation time
index_first = np.argmin(arrival_times) # find the reference microphone (the nearest to the source)
# output: index of the minimum value

relative_delays = arrival_times - np.min(arrival_times) # these represent the relative delays between the reference mic and the other mics

# PARAMETERS VALUE PRINTED
print("Microphone positions:")
print(mic_x)

print("\nDistances:")
print(distances)

print("\nArrival times:")
print(arrival_times)

print("\nFirst microphone index:")
print(index_first)

print("\nRelative delays:")
print(relative_delays)

# PLOT

plt.figure(figsize=(9, 7))
for i in range(M):
    plt.plot([source_x, mic_x[i]], [source_y, mic_y[i]], linestyle = "--", alpha = 0.4)

# Microphones
plt.scatter(mic_x, mic_y, label = "Microphones")
plt.scatter(source_x, source_y, marker = "x", s = 100, label = "source")

plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Source - Microphone Array Geometry")

plt.grid()
plt.axis("equal")
plt.legend()

# IMPORTANT: actually display the plot
plt.show()



