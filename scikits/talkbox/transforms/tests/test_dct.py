import numpy as np
from numpy.testing import TestCase, assert_array_almost_equal

from scikits.talkbox.transforms.dct_ref import direct_dctii, direct_dctii_2
from scikits.talkbox.transforms.dct import dctii

class TestDCTTypeII(TestCase):
    Y0 = np.array([16.58312395177700, -10.41945851392763, 0.,
        -1.12380254641222, -0., -0.37572376864581, -0., -0.16287097213722,
        0., -0.06524422831323, 0.])

    Y1 = np.array([15.81138830084189, -10.02761236237870, 0,
        -1.07406322530303, 0, -0.35136418446315, 0, -0.14207821409532, 0,
        -0.03984144487100])

    X0 = np.linspace(0, 10, 11)
    X1 = np.linspace(0, 10, 10)

    def test_simple_direct(self):
        """Test 1d input, direct implementation."""
        assert_array_almost_equal(self.Y0, direct_dctii(self.X0))
        assert_array_almost_equal(self.Y1, direct_dctii(self.X1))

    def test_simple_direct2(self):
        """Test 1d input, 2nd direct implementation."""
        assert_array_almost_equal(self.Y0, direct_dctii_2(self.X0))
        assert_array_almost_equal(self.Y1, direct_dctii_2(self.X1))

    def test_simple(self):
        """Test 1d input, fft implementation."""
        assert_array_almost_equal(self.Y0, dctii(self.X0))
        assert_array_almost_equal(self.Y1, dctii(self.X1))
