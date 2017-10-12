import math, sys
import pylab as pl
sys.path.append ('/home/bluewhite/Project/mypy')
from CMC_file import *

FILE = '../compareED/LA1X_5.0_equi.obs'
if sys.argv[0] != 0: FILE = sys.argv[1]

def _geterr (sum_, sqrsum_, len_):
  mean = sum_ / float(len_)
  return math.sqrt (sqrsum_/float(len_) - mean*mean) / float(len_)

def analy (raw):
  _name, _sum, _sqrsum, _count, _mean, _err = '', 0., 0., 0, [], []
  _name = raw[0]
  for i in range(1,len(raw)):
    _count += 1
    _sum += raw[i]
    _sqrsum += raw[i]*raw[i]
    _mean.append (_sum/float(_count))
    _err.append (_geterr(_sum, _sqrsum, _count))
  return _mean, _err

# Read and analysis
raw = readfile (FILE)
for rawi in raw:
  dat = ['',[],[],[]]
  dat[0], dat[1] = (rawi[0]), range(len(rawi)-2)
  dat[2], dat[3] = analy (rawi[1:])
  # Plot
  pl.errorbar (dat[1], dat[2], dat[3], label=dat[0])
pl.legend()
pl.show()
