import numpy as np
from numpy.testing import TestCase, assert_array_almost_equal

from scikits.talkbox.tools.segmentaxis import segment_axis

class TestSegmentAxis(TestCase):
    def test1(self):
        x = np.linspace(0, 9, 10)

        y = segment_axis(x, 4)
        assert_array_almost_equal(y, np.array([[0, 1, 2, 3], [4, 5, 6, 7]]))

        y = segment_axis(x, 4, 2)
        assert_array_almost_equal(y, np.array([[0, 1, 2, 3], [2, 3, 4, 5], 
                                               [4, 5, 6, 7], [6, 7, 8, 9]]))

        y = segment_axis(x, 3, 2)
        assert_array_almost_equal(y, np.array([[0, 1, 2], [1, 2, 3], 
                                               [2, 3, 4], [3, 4, 5],
                                               [4, 5, 6], [5, 6, 7],
                                               [6, 7, 8], [7, 8, 9]]))

        y = segment_axis(x, 4, 3)
        assert_array_almost_equal(y, np.array([[0, 1, 2, 3], [1, 2, 3, 4], 
                                               [2, 3, 4, 5], [3, 4, 5, 6],
                                               [4, 5, 6, 7], [5, 6, 7, 8],
                                               [6, 7, 8, 9]]))

