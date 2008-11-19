import numpy as np
from numpy.testing import TestCase, assert_array_almost_equal

from scipy.signal import lfilter

from scikits.talkbox.tools.ffilter import slfilter

class TestFfilter(TestCase):
    def setUp(self):
        self.func = slfilter

    def test1(self):
        x = np.random.randn(2, 10)
        b = np.random.randn(2, 2)
        a = np.random.randn(2, 3)

        y = self.func(b, a, x)
        for i in range(x.shape[0]):
            yr = lfilter(b[i], a[i], x[i])
            assert_array_almost_equal(y[i], yr)
