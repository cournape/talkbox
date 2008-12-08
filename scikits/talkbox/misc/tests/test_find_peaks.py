import numpy as np
from numpy.testing import TestCase, assert_array_equal, \
                          assert_array_almost_equal, dec

from scikits.talkbox.misc.peak_picking import find_peaks

class TestFindPeaks(TestCase):
    def test_simple(self):
        x = np.sin(np.linspace(0, 6 * np.pi, 256))
        p = find_peaks(x, 10)
        assert_array_equal(p, [21, 106, 191, 255])

if __name__ == "__main__":
    run_module_suite()
