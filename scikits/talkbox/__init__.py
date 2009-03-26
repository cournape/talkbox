__all__ = []

from tools import *
import tools
__all__ += tools.__all__

import linpred
from linpred import *
__all__ += linpred.__all__

import version

from numpy.testing import Tester

test = Tester().test
bench = Tester().bench
