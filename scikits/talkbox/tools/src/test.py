import numpy as np
from scipy.signal import lfilter

from scikits.talkbox.tools.correlations import acorr

from cffilter import cslfilter as lfilter2
from cacorr import acorr as cacorr

# def f1(b, a, x):
#     y = np.empty(x.shape, x.dtype)
# 
#     for i in range(y.shape[0]):
#         y[i] = lfilter(b[i], a[i], x[i])
#     return y
# 
# def f2(b, a, x):
#     return lfilter2(b, a, x)
# 
# nframes = 3600
# a = np.random.randn(nframes, 1)
# #a = np.array([[1], [-1]])
# b = np.random.randn(nframes, 24)
# #b = np.array([[1, 1], [1, 1]])
# x = np.random.randn(nframes, 256)
# #x = np.linspace(0, 19, 20).reshape((2, 10))
# 
# y = f1(b, a, x)
# yr = f2(b, a, x)
# np.testing.assert_array_almost_equal(y, yr)

x = np.random.randn(1, 5)

maxlag = 1
onesided = False
axis = 1
nx = x.shape[1]
y = cacorr(x, maxlag, onesided, axis)
r_y = acorr(x, axis, onesided)

#print y
#print r_y
np.testing.assert_array_almost_equal(y, r_y[:,nx-maxlag-1:nx+maxlag])
