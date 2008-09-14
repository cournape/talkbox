import numpy as np
from numpy.testing import assert_array_almost_equal
from unittest import TestCase

from scikits.talkbox.lpc.py_lpc import lpc_ref, levinson_1d as py_levinson
from scikits.talkbox.lpc._lpc import levinson as c_levinson
from scikits.talkbox.lpc import levinson

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

    def setUp(self):
        self.lpc_func = lpc_ref

    def test_order0(self):
        """Testing lpc ref order 0."""
        assert_array_almost_equal(self.X0, self.lpc_func(self.X, 0))

    def test_order1(self):
        """Testing lpc ref order 1."""
        assert_array_almost_equal(self.X1, self.lpc_func(self.X, 1))

    def test_order2(self):
        """Testing lpc ref order 2."""
        assert_array_almost_equal(self.X2, self.lpc_func(self.X, 2))

    def test_order5(self):
        """Testing lpc ref order 5."""
        assert_array_almost_equal(self.X5, self.lpc_func(self.X, 5))

    def test_order10(self):
        """Testing lpc ref order 10."""
        assert_array_almost_equal(self.X10, self.lpc_func(self.X, 10))

    def test_order11(self):
        """Testing lpc ref order 11."""
        assert_array_almost_equal(self.X11, self.lpc_func(self.X, 11))

class _LevinsonCommon(TestCase):
    X = np.linspace(1, 11, 11)
    X0 = np.array([1.])
    X1 = np.array([1, -2.])
    X5 = np.array([1, -1.166666666667, 0., 0., -0., -0.166666666667])
    X10 = np.array([1., -1.0909090909, 0, 0, 0, 0, 0, 0, 0, 0, -0.09090909])

    Xc = np.linspace(1, 11, 11) + 1.j * np.linspace(0, 10, 11)
    Xc1 = np.array([1, -2-1j])
    Xc5 = np.array([1., -1.2, 0, 0, 0, -0.2000j])
    Xc10 = np.array([1., -1.1, 0, 0, 0, 0, 0, 0, 0, 0, -0.1j])

    Xm = np.linspace(1, 11 * 8, 11 * 8).reshape(8, 11)
    Xm0_a0 = np.ones(11, dtype = Xm.dtype)[None, :]
    Xm1_a0 = np.array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                       [-0.8027, -0.8052, -0.8076, -0.8100, -0.8122, -0.8143,
                        -0.8163, -0.8182, -0.8201, -0.8218, -0.8235]])
    Xm5_a0 = np.array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                       [-0.8602, -0.8623, -0.8643, -0.8662, -0.8681, -0.8698,
                        -0.8715, -0.8730, -0.8745, -0.8759, -0.8773],
                       [0.0235, 0.0229, 0.0223, 0.0218, 0.0213, 0.0207, 0.0202,
                        0.0198, 0.0193, 0.0188, 0.0184],
                       [0.0247, 0.0241, 0.0234, 0.0228, 0.0223, 0.0217, 0.0211,
                        0.0206, 0.0201, 0.0196, 0.0191],
                       [0.0268, 0.0260, 0.0253, 0.0246, 0.0240, 0.0233, 0.0227,
                        0.0221, 0.0215, 0.0210, 0.0204],
                       [0.0425, 0.0428, 0.0432, 0.0436, 0.0440, 0.0445, 0.0449,
                        0.0454, 0.0460, 0.0465, 0.0470]])

    def setUp(self):
        self.levinson_func = None

    def test_simpl0(self):
        assert_array_almost_equal(self.levinson_func(self.X, 0)[0], self.X0)

    def test_simple1(self):
        assert_array_almost_equal(self.levinson_func(self.X, 1)[0], self.X1)

    def test_simple2(self):
        assert_array_almost_equal(self.levinson_func(self.X, 5)[0], self.X5)
        assert_array_almost_equal(self.levinson_func(self.X, 10)[0], self.X10)

class TestLevinsonPyBackend(_LevinsonCommon):
    def setUp(self):
        self.levinson_func = py_levinson

    def test_complex(self):
        assert_array_almost_equal(self.levinson_func(self.Xc, 1)[0], self.Xc1)
        assert_array_almost_equal(self.levinson_func(self.Xc, 5)[0], self.Xc5)
        assert_array_almost_equal(self.levinson_func(self.Xc, 10)[0], self.Xc10)

class TestLevinsonCBackend(_LevinsonCommon):
    def setUp(self):
        self.levinson_func = c_levinson

class TestLevinson(_LevinsonCommon):
    def setUp(self):
        self.levinson_func = levinson

        self.ref = {}
        self.ref[0] = {0: self.Xm0_a0, 1: self.Xm1_a0, 5: self.Xm1_a0}
        #self.ref[1] = {0: self.Xm0_a0, 1: self.Xm1_a0, 5: self.Xm5_a1}

    def test_axis(self):
        for axis in [0]:
            for order in [0, 1, 5]:
                a, e, k = self.levinson_func(self.Xm, order, axis)
                assert_array_almost_equal(self.ref[axis][order], a)
