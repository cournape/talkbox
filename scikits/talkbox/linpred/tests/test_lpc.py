import numpy as np
from numpy.testing import *
from unittest import TestCase

from scipy.signal import lfilter

from scikits.talkbox.tools import acorr

from scikits.talkbox.linpred.py_lpc import lpc_ref, levinson_1d as py_levinson
from scikits.talkbox.linpred._lpc import levinson as c_levinson
from scikits.talkbox.linpred.levinson_lpc import levinson, acorr_lpc, lpc
from scikits.talkbox.linpred.common import lpcres

def test_acorr_lpc():
    x = np.random.randn(12, 5)
    y = acorr_lpc(x)
    assert_array_equal(y[:, :5], acorr(x, onesided=True)/5)
    assert_array_almost_equal(y[:, 5], np.zeros(y.shape[0], y.dtype))

    y = acorr_lpc(x, axis=0)
    assert_array_equal(y[:12,:], acorr(x, axis=0, onesided=True)/12)
    assert_array_almost_equal(y[12, 0], np.zeros((1, y.shape[1]), y.dtype))

class _TestLPCCommon(TestCase):
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

class TestLPCPyBackend(_TestLPCCommon):
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

class TestLPCHighBackend(_TestLPCCommon):
    E0 = np.array([35.])
    E1 = np.array([9.28571428571428])
    E5 = np.array([9.15927742966687])
    E10 = np.array([9.13002661779096])

    def setUp(self):
        from scikits.talkbox.linpred.levinson_lpc import lpc
        self.lpc = lpc

    def test_pred_err(self):
        err = self.lpc(self.X, 0)[1]
        assert_array_almost_equal(self.E0, err)

        err = self.lpc(self.X, 1)[1]
        assert_array_almost_equal(self.E1, err)

        err = self.lpc(self.X, 5)[1]
        assert_array_almost_equal(self.E5, err)

        err = self.lpc(self.X, 10)[1]
        assert_array_almost_equal(self.E10, err)

    def test_order0(self):
        """Testing actual lpc order 0."""
        assert_array_almost_equal(self.X0, self.lpc(self.X, 0)[0])

    def test_order1(self):
        """Testing actual lpc order 1."""
        assert_array_almost_equal(self.X1, self.lpc(self.X, 1)[0])

    def test_order2(self):
        """Testing actual lpc order 2."""
        assert_array_almost_equal(self.X2, self.lpc(self.X, 2)[0])

    def test_order5(self):
        """Testing actual lpc order 5."""
        assert_array_almost_equal(self.X5, self.lpc(self.X, 5)[0])

    def test_order10(self):
        """Testing actual lpc order 10."""
        assert_array_almost_equal(self.X10, self.lpc(self.X, 10)[0])

    def test_order11(self):
        """Testing actual lpc order 11."""
        assert_array_almost_equal(self.X11, self.lpc(self.X, 11)[0])

    def test_axisdef(self):
        """Testing lpc of matrix, along default axis."""
        xm = np.vstack((self.X, self.X))
        re = {0: self.X0, 1: self.X1, 2: self.X1, 5: self.X5, 10: self.X10,
              11: self.X11}
        for order in [0, 1, 5, 10, 11]:
            am = self.lpc(xm, order=order)[0]
            for i in range(2):
                assert_array_almost_equal(am[i], re[order])

    def test_axis0(self):
        """Testing lpc of matrix, along axis 0."""
        xm = np.vstack((self.X, self.X)).T
        re = {0: self.X0.T, 1: self.X1.T, 2: self.X1.T, 5: self.X5.T,
              10: self.X10.T, 11: self.X11.T}

        for order in [0, 1, 5, 10, 11]:
            am = self.lpc(xm, order=order, axis=0)[0]
            for i in range(2):
                assert_array_almost_equal(am[:, i], re[order])

class _LevinsonCommon(TestCase):
    X = np.linspace(1, 11, 11)
    X0 = np.array([1.])
    E0 = np.array([1.])
    X1 = np.array([1, -2.])
    E1 = np.array([-3.])
    X5 = np.array([1, -1.166666666667, 0., 0., -0., -0.166666666667])
    E5 = np.array([-7/3.])
    X10 = np.array([1., -1.0909090909, 0, 0, 0, 0, 0, 0, 0, 0, -0.09090909])
    E10 = np.array([-2.181818181818181818])

    Xc = np.linspace(1, 11, 11) + 1.j * np.linspace(0, 10, 11)
    Xc1 = np.array([1, -2-1j])
    Xc5 = np.array([1., -1.2, 0, 0, 0, -0.2000j])
    Xc10 = np.array([1., -1.1, 0, 0, 0, 0, 0, 0, 0, 0, -0.1j])

    Xm = np.linspace(1, 11 * 8, 11 * 8).reshape(8, 11)
    Xm0_a0 = np.ones(11, dtype = Xm.dtype)[None, :]
    Xm1_a0 = np.array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
                       [-12., -6.5, -4.66666667,-3.75, -3.2, -2.83333333,
                        -2.57142857, -2.375, -2.22222222, -2.1, -2.]])

    Xm7_a0 = np.array([[ 1.00000000e+00,  1.00000000e+00,  1.00000000e+00,
                         1.00000000e+00,  1.00000000e+00,  1.00000000e+00,
                         1.00000000e+00,  1.00000000e+00,  1.00000000e+00,
                         1.00000000e+00,  1.00000000e+00],
                       [-1.16176471e+00, -1.15714286e+00, -1.15277778e+00,
                        -1.14864865e+00, -1.14473684e+00, -1.14102564e+00,
                        -1.13750000e+00, -1.13414634e+00, -1.13095238e+00,
                        -1.12790698e+00, -1.12500000e+00],
                       [ 3.77160714e-16,  2.69210799e-16, -3.13275572e-16,
                        -8.29044746e-17,  2.95247607e-16, -4.08063714e-16,
                        -4.68392740e-16, -4.26474168e-17,  4.06293718e-16,
                         2.76281560e-16,  3.26921030e-16],
                       [-5.17219625e-16,  2.29608624e-16, -3.11123397e-18,
                         1.94303455e-16, -2.79400340e-16,  2.45641928e-16,
                         3.90477982e-16,  2.57888073e-16, -3.08179809e-16,
                        -4.84799075e-16, -4.02802791e-16],
                       [ 5.04820884e-16, -6.10790554e-16,  5.86895205e-16,
                        -4.02859774e-16,  3.04278315e-16, -2.12894415e-17,
                        -3.58539724e-16, -1.56583906e-16,  4.94802637e-16,
                         2.63602992e-16,  1.12410081e-16],
                       [-8.17830928e-16,  6.59761772e-17, -1.96108036e-16,
                         7.72307387e-16,  1.20311579e-16,  3.03438805e-17,
                         3.63943041e-16, -2.12327864e-16, -4.62399256e-16,
                        -8.99413171e-17, -9.55089182e-17],
                       [ 5.55111512e-16,  8.32667268e-17, -2.22044605e-16,
                        -4.99600361e-16, -2.22044605e-16, -2.49800181e-16,
                         8.32667268e-17,  2.77555756e-16, -4.71844785e-16,
                         4.16333634e-16,  6.93889390e-16],
                       [-1.61764706e-01, -1.57142857e-01, -1.52777778e-01,
                        -1.48648649e-01, -1.44736842e-01, -1.41025641e-01,
                        -1.37500000e-01, -1.34146341e-01, -1.30952381e-01,
                        -1.27906977e-01, -1.25000000e-01]])

    Xm0_a1 = np.ones(8, dtype = Xm.dtype)[:, None]
    Xm1_a1 = np.array([[ 1., -2.],
                       [ 1., -1.08333333],
                       [ 1., -1.04347826],
                       [ 1., -1.02941176],
                       [ 1., -1.02222222],
                       [ 1., -1.01785714],
                       [ 1., -1.01492537],
                       [ 1., -1.01282051]])
    Xm10_a1 = np.array([[ 1.00000000e+00, -1.09090909e+00,  2.48368345e-17,
                          4.17212761e-16, -2.00924534e-16, -3.98863242e-16,
                          9.92384986e-16, -1.44931966e-15,  6.03318301e-16,
                         -3.05311332e-16, -9.09090909e-02],
                        [ 1.00000000e+00, -1.03030303e+00, -1.22247501e-17,
                          1.36023073e-15, -4.48031297e-16, -1.35490509e-15,
                          1.52774273e-15, -6.93512486e-16,  1.74736602e-15,
                         -1.17267307e-15, -3.03030303e-02],
                        [ 1.00000000e+00, -1.01818182e+00,  2.56033011e-15,
                         -1.13471667e-15, -1.51893003e-15,  2.05757192e-16,
                          3.02007915e-15, -1.40321656e-15, -2.57416563e-17,
                          1.94982919e-15, -1.81818182e-02],
                        [ 1.00000000e+00, -1.01298701e+00,  2.44192998e-15,
                          5.20720957e-16, -5.48776475e-16,  2.10655840e-15,
                         -5.80572636e-15,  3.77248850e-15,  1.38878553e-15,
                         -2.35575448e-15, -1.29870130e-02],
                        [ 1.00000000e+00, -1.01010101e+00,  1.88495917e-15,
                          6.41223658e-16,  1.18580041e-15, -7.72270515e-16,
                         -2.62575027e-15,  4.40437387e-15, -4.99371930e-15,
                         -1.64798730e-15, -1.01010101e-02],
                        [ 1.00000000e+00, -1.00826446e+00,  4.40941636e-15,
                         -9.91551517e-16, -2.32484424e-15,  6.43021235e-17,
                         -9.08245602e-16,  1.81345488e-15,  2.49768366e-16,
                          2.12850571e-15, -8.26446281e-03],
                        [ 1.00000000e+00, -1.00699301e+00, -4.33078097e-15,
                          6.28478928e-15, -4.81227239e-15, -3.26880638e-15,
                          8.58692579e-15, -2.27870777e-15, -1.40252634e-15,
                          3.99680289e-15, -6.99300699e-03],
                        [ 1.00000000e+00, -1.00606061e+00,  3.47394667e-15,
                         -1.59763597e-15, -5.28108333e-15,  1.07369329e-14,
                         -5.53240143e-15, -3.20313334e-15, -5.92624612e-16,
                          6.94756752e-16, -6.06060606e-03]])

    # References for prediction error
    referr = {0: E0, 1: E1, 5: E5, 10: E10}

    def setUp(self):
        self.levinson_func = None

    def test_simpl0(self):
        assert_array_almost_equal(self.levinson_func(self.X, 0)[0], self.X0)

    def test_simple1(self):
        assert_array_almost_equal(self.levinson_func(self.X, 1)[0], self.X1)

    def test_simple2(self):
        assert_array_almost_equal(self.levinson_func(self.X, 5)[0], self.X5)
        assert_array_almost_equal(self.levinson_func(self.X, 10)[0], self.X10)

    def test_error_rank1(self):
        for order in [0, 1, 5, 10]:
            a, e, k = self.levinson_func(self.X, order)
            assert_array_almost_equal(self.referr[order], e)

    def test_arg_handling(self):
        # Check Order
        try:
            self.levinson_func(self.X0, 1)
            self.fail("levinson func succeed with bad argument !")
        except ValueError, e:
            assert str(e) == "Order should be <= size-1"

        # Check empty input
        try:
            self.levinson_func([], 1)
            self.fail("levinson func succeed with bad argument !")
        except ValueError, e:
            assert str(e) == "Cannot operate on empty array !"

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

        # References for filter coefficients
        self.ref = {}
        self.ref[0] = {0: self.Xm0_a0, 1: self.Xm1_a0, 7: self.Xm7_a0}
        self.ref[1] = {0: self.Xm0_a1, 1: self.Xm1_a1, 10: self.Xm10_a1}

    def test_axis0(self):
        for order in [0, 1, 7]:
            a, e, k = self.levinson_func(self.Xm, order, 0)
            assert_array_almost_equal(self.ref[0][order], a)

    def test_axis1(self):
        for order in [0, 1, 10]:
            a, e, k = self.levinson_func(self.Xm, order, 1)
            assert_array_almost_equal(self.ref[1][order], a)

class TestLPCResidual(TestCase):
    def test_simple(self):
        """Testing LPC residual of one signal."""
        x = np.linspace(0, 10, 11)
        r_res = np.array([0.,  1.,  1.08531469, 1.23776224, 1.39020979,
                          1.54265734, 1.6951049, 1.84755245, 2., 2.15244755,
                          2.3048951 ])

        res = lpcres(x, 2) 
        assert_array_almost_equal(res, r_res)

    def test_r2(self):
        """Testing LPC residual of a set of windows."""
        order = 12
        x = np.random.randn(10, 24)

        res = lpcres(x, order)
        r_res = np.empty(x.shape, x.dtype)
        for i in range(10):
            r_res[i] = lfilter(lpc(x[i], order)[0], 1., x[i])

        assert_array_almost_equal(res, r_res)

        res = lpcres(x, order, usefft=False)
        assert_array_almost_equal(res, r_res)

if __name__ == "__main__":
    run_module_suite()
