import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.spectral.basic import periodogram
from scipy.signal import hamming, hanning
fs = 1000
x = np.sin(2 * np.pi * 0.15 * fs * np.linspace(0., 0.3, 0.3 * fs))
x += 0.1 * np.random.randn(x.size)
px1, fx1 = periodogram(x, nfft=16384, fs=fs)
px2, fx2 = periodogram(x * hamming(x.size), nfft=16384, fs=fs)
plt.subplot(2, 1, 1)
plt.plot(fx1, 10 * np.log10(px1))
plt.subplot(2, 1, 2)
plt.plot(fx2, 10 * np.log10(px2))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.savefig('periodogram_2.png')
