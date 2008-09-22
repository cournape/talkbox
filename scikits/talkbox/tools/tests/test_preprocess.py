import numpy as np
from numpy.testing import *
       
from scikits.talkbox.tools.preprocess import demean

class TestDeman(TestCase):
    def test1(self):
        a = np.array([1, 3, 1, 3])

        assert_array_equal(demean(a), 
                           np.array([-1, 1, -1, 1]))

    def test2(self):
        a = np.array([[1, 3], [1, 3]])

        assert_array_equal(demean(a), 
                           np.array([[-1, 1], [-1, 1]]))

        assert_array_equal(demean(a,0), 
                           np.zeros((2, 2), a.dtype))

