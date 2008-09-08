import numpy as np
from numpy.testing import assert_array_almost_equal
from unittest import TestCase

from scikits.talkbox.lpc.lpc import lpc_ref, levinson

class TestLPC(TestCase):
    # Values taken from matlab LPC
    X = np.linspace(0, 10, 11)
    X0 = np.array([1.])
    X1 = np.array([1., -0.85714285714286])
    X2 = np.array([1., -0.91468531468532, 0.06713286713287])
    X5 = np.array([1., -0.90444817959784, 0.01158960447639, 0.01191036566532,
                   0.01244767895726, 0.04749964947373])
    X10 = np.array([1., -0.90129704880529, 0.01182431679473, 0.01215800819372,
                    0.01271275428716, 0.01349864136763, 0.01452995829115,
                    0.01582545627451, 0.01740868982649, 0.01930844501169,
                    -0.03162073915296])
    X11 = np.array([1., -0.89945522397677, 0.01069965069345, 0.01114399783175,
                    0.01179096311245, 0.01265230954064, 0.01374369796049,
                    0.01508497179779, 0.01670051784961, 0.01861970968050,
                    0.02087744168741, -0.05824736795705])

    def test_order0(self):
        """Testing lpc ref order 0."""
        assert_array_almost_equal(self.X0, lpc_ref(self.X, 0))

    def test_order1(self):
        """Testing lpc ref order 1."""
        assert_array_almost_equal(self.X1, lpc_ref(self.X, 1))

    def test_order2(self):
        """Testing lpc ref order 2."""
        assert_array_almost_equal(self.X2, lpc_ref(self.X, 2))

    def test_order5(self):
        """Testing lpc ref order 5."""
        assert_array_almost_equal(self.X5, lpc_ref(self.X, 5))

    def test_order10(self):
        """Testing lpc ref order 10."""
        assert_array_almost_equal(self.X10, lpc_ref(self.X, 10))

    def test_order11(self):
        """Testing lpc ref order 11."""
        assert_array_almost_equal(self.X11, lpc_ref(self.X, 11))

class TestLevinson(TestCase):
    X = np.linspace(1, 11, 11)
    X0 = np.array([1.])
    X1 = np.array([1, -2.])
    X5 = np.array([1, -1.166666666667, 0., 0., -0., -0.166666666667])
    X10 = np.array([1., -1.0909090909, 0, 0, 0, 0, 0, 0, 0, 0, -0.09090909])

    Xc = np.linspace(1, 11, 11) + 1.j * np.linspace(0, 10, 11)
    Xc1 = np.array([1, -2-1j])
    Xc5 = np.array([1., -1.2, 0, 0, 0, -0.2000j])
    Xc10 = np.array([1., -1.1, 0, 0, 0, 0, 0, 0, 0, 0, -0.1j])


    def test_simpl0(self):
        assert_array_almost_equal(levinson(self.X, 0)[0], self.X0)

    def test_simple1(self):
        assert_array_almost_equal(levinson(self.X, 1)[0], self.X1)

    def test_simple2(self):
        assert_array_almost_equal(levinson(self.X, 5)[0], self.X5)
        assert_array_almost_equal(levinson(self.X, 10)[0], self.X10)

    def test_complex(self):
        assert_array_almost_equal(levinson(self.Xc, 1)[0], self.Xc1)
        assert_array_almost_equal(levinson(self.Xc, 5)[0], self.Xc5)
        assert_array_almost_equal(levinson(self.Xc, 10)[0], self.Xc10)
