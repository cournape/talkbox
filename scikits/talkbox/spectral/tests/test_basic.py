from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_almost_equal

from scikits.talkbox.spectral.basic import periodogram

lh = np.array([2.4, 2.4, 2.4, 2.2, 2.1, 1.5, 2.3, 2.3, 2.5, 2.0, 1.9, 1.7,
2.2, 1.8, 3.2, 3.2, 2.7, 2.2, 2.2, 1.9, 1.9, 1.8, 2.7, 3.0, 2.3, 2.0, 2.0, 2.9,
2.9, 2.7, 2.7, 2.3, 2.6, 2.4, 1.8, 1.7, 1.5, 1.4, 2.1, 3.3, 3.5, 3.5, 3.1, 2.6,
2.1, 3.4, 3.0, 2.9])

# Returned by p = spectrum(lh, plot=FALSE, detrend=FALSE, taper=0.0)
# XXX: R drops the first item (DC component) of the estimated spectrogram
lh_spec_raw = np.array([0.32650971, 0.79865114, 1.25684523, 0.66284366,
0.13803913, 1.51075717, 0.23526771, 0.66520833, 0.28393413, 0.09545270,
0.24710226, 0.18541667, 0.02353390, 0.07176963, 0.05049468, 0.11312500,
0.02028320, 0.04174283, 0.09056918, 0.01548967, 0.02039262, 0.11912653,
0.16702824, 0.02083333])

class TestSpecgram(TestCase):
    def test_raw(self):
        sp = periodogram(lh)[0]
        assert_array_almost_equal(sp[1:], lh_spec_raw)
