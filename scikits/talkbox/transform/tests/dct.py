import numpy as np
from numpy.testing import *

from scikits.talkbox.transform.dct import direct_dctii

class TestDCTII(TestCase):
    def test_simple(self):
        X0 = np.linspace(0, 10, 11)
        X1 = np.linspace(0, 10, 10)

        Y0 = np.array([16.58312395177700, -10.41945851392763, 0.,
            -1.12380254641222, -0., -0.37572376864581, -0., -0.16287097213722,
            0., -0.06524422831323, 0.])

        Y1 = np.array([15.81138830084189, -10.02761236237870, 0,
            -1.07406322530303, 0, -0.35136418446315, 0, -0.14207821409532, 0,
            -0.03984144487100])

        assert_array_almost_equal(Y0, dct(X0))
        assert_array_almost_equal(Y1, dct(X1))
