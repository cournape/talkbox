from linpred import *
import linpred
__all__ = linpred.__all__

from tools import *
import tools
__all__ += tools.__all__

from numpy.testing import Tester

test = Tester().test
bench = Tester().bench
