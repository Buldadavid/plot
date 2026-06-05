import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

plt.style.use('moje.mplstyle')

#####################nacteni dat####################################

# data = np.genfromtxt(r"S:\Moving from min to max 85% speed 38C.CSV", delimiter=',', skip_header=1)
# 
# t       =   data[: , 0][250:]  # čas (ms)
# r479    =   data[: , 1][250:]  # Diagnostická pozice enkoderu (r479[0])
# r93     =   data[: , 2][250:]  # úhel pouzice el. (°) (r93)
# r94     =   data[: , 3][250:]  # transformační úhel (°) (r94)
# r61     =   data[: , 4][250:]  # otáčky nevhlazené (rpm) (r61[0])
# r63     =   data[: , 5][250:]  # otáčky vyhlazené (rpm) (r63)
# r9714   =   data[: , 6][250:]  # rychlost posuvu (mm/min) (r9714[0])
# r69     =   data[: , 7][250:]  # proud fáze (A) (r69[0])
# 

#####################nacteni dat####################################

data = np.genfromtxt(r"S:\1.FILE\pok\DRYLOCK60-Ok.CSV", delimiter=',', skip_header=1)

t  = data[: , 0]
r61 = data[: , 1]
r63 = data[: , 2]
r69 = data[: , 3]

#####################vykreslení dat####################################

plt.figure(figsize=(12, 12))

plt.subplot(4, 1, 1)
plt.plot(t, r61, label = "otáčky nevyhlazené")
plt.plot(t, r63, label = "otáčky vyhlazené")
plt.xlabel('Čas [ms]')
plt.ylabel('rychlost [rpm]')
plt.ylim(0,250)
plt.legend()
plt.title('otáčky motoru')

sample_rate = 1/((t[1]-t[0])/1e3)  # Vzorkovací frekvence v Hz (např. 1000 vzorků za sekundu) 
signal = r61 - np.mean(r61)
signalb = r63 - np.mean(r63)
# --- Volitelná vizualizace ---

Na = len(signal)
Ta = 1/sample_rate
yfa = fft(signal)
xfa = fftfreq(Na, Ta)[:Na//2]

Nb = len(signalb)
Tb = 1/sample_rate
yfb = fft(signalb)
xfb = fftfreq(Nb, Tb)[:Nb//2]

plt.subplot(4, 1, 2)
plt.plot(xfa, 2.0/Na * np.abs(yfa[0:Na//2]), label = "r61")
plt.plot(xfb, 2.0/Nb * np.abs(yfb[0:Nb//2]), label = "r63")

plt.title('Frekvenční spektrum (FFT) otáček r61')
plt.xlabel('Frekvence [Hz]')
plt.ylabel('Amplituda (normalizovaná)')
plt.grid(True)

#plt.ylim(0, 3)
plt.xlim(0, 125) # Omezíme zobrazení na zajímavou část spektra

plt.subplot(4, 1, 3)
plt.title(r"Proud fáze U r69")
plt.plot(t, r69, label = "proud fáze (r69[0])")
plt.xlabel('Čas [ms]')
plt.ylabel('proud fáze [A] ')
plt.xlim(1000,2000)
plt.ylim(-10,10)
plt.legend()

sample_rate = 1 / (t[1]-t[0])/1e-3 #1/2e-3  # Vzorkovací frekvence v Hz
Na = len(r69)
Ta = 1/sample_rate
yfa = fft(r69)
xfa = fftfreq(Na, Ta)[:Na//2]

plt.subplot(4, 1, 4)
plt.plot(xfa, 2.0/Na * np.abs(yfa[0:Na//2]))

plt.title('Frekvenční spektrum (FFT) proudu fáze U (r69[0])')
plt.xlabel('Frekvence [Hz]')
plt.ylabel('Amplituda (normalizovaná)')
plt.grid(True)

plt.ylim(0, 0.2)
plt.xlim(0, 125)

plt.tight_layout()
plt.show()

#print(xfa[np.where(2.0/Na * np.abs(yfa[0:Na//2]) == max(2.0/Na * np.abs(yfa[0:Na//2])[:int(np.floor((len(xfa)/125)*40))]))[0][0]],"hz")