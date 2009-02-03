import numpy as np
from numpy.testing import TestCase, assert_array_almost_equal, assert_equal

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


    def test_simple(self):
        assert_equal(segment_axis(np.arange(6),length=3,overlap=0),
                         np.array([[0,1,2],[3,4,5]]))

        assert_equal(segment_axis(np.arange(7),length=3,overlap=1),
                         np.array([[0,1,2],[2,3,4],[4,5,6]]))

        assert_equal(segment_axis(np.arange(7),length=3,overlap=2),
                         np.array([[0,1,2],[1,2,3],[2,3,4],[3,4,5],[4,5,6]]))

    def test_error_checking(self):
        self.assertRaises(ValueError,
                lambda: segment_axis(np.arange(7),length=3,overlap=-1))
        self.assertRaises(ValueError,
                lambda: segment_axis(np.arange(7),length=0,overlap=0))
        self.assertRaises(ValueError,
                lambda: segment_axis(np.arange(7),length=3,overlap=3))
        self.assertRaises(ValueError,
                lambda: segment_axis(np.arange(7),length=8,overlap=3))

    def test_ending(self):
        assert_equal(segment_axis(np.arange(6),length=3,overlap=1,end='cut'),
                         np.array([[0,1,2],[2,3,4]]))
        assert_equal(segment_axis(np.arange(6),length=3,overlap=1,end='wrap'),
                         np.array([[0,1,2],[2,3,4],[4,5,0]]))
        assert_equal(segment_axis(np.arange(6),length=3,overlap=1,end='pad',endvalue=-17),
                         np.array([[0,1,2],[2,3,4],[4,5,-17]]))

    def test_multidimensional(self):
        
        assert_equal(segment_axis(np.ones((2,3,4,5,6)), axis=3, length=3, 
                                  overlap=1).shape, (2,3,4,2,3,6))

        assert_equal(segment_axis(np.ones((2,5,4,3,6)).swapaxes(1,3), 
                                  axis=3, length=3, overlap=1).shape,
                     (2,3,4,2,3,6))

        assert_equal(segment_axis(np.ones((2,3,4,5,6)), axis=2, length=3,
            overlap=1, end='cut').shape,
                     (2,3,1,3,5,6))

        assert_equal(segment_axis( 
                np.ones((2,3,4,5,6)), axis=2, length=3, overlap=1, end='wrap').shape,
                     (2,3,2,3,5,6))

        assert_equal(segment_axis(
                np.ones((2,3,4,5,6)), axis=2, length=3, overlap=1, end='pad').shape,
                     (2,3,2,3,5,6))
