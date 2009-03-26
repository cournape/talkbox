import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.spectral.basic import periodogram
fs = 1000
x = np.sin(2 * np.pi * 0.15 * fs * np.linspace(0., 0.3, 0.3 * fs))
x += 0.1 * np.random.randn(x.size)
px, fx = periodogram(x, nfft=16384, fs=fs)
plt.plot(fx, 10 * np.log10(px))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.savefig('periodogram_1.png')
