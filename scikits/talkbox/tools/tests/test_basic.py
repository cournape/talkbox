import numpy as np
from numpy.testing import TestCase, assert_array_equal

from scikits.talkbox.tools.acorr import nextpow2

class TestNextpow2(TestCase):
    X = np.array([0, 1, 2, 3, 4, 6, 8, 15, 16, 17, 32, np.nan, np.infty])
    Y = np.array([0., 0, 1, 2, 2, 3, 3, 4, 4, 5, 5, np.nan, np.infty])
    def test_simple(self):
        assert_array_equal(nextpow2(self.X), self.Y)
