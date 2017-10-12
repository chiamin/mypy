import sys, os
sys.path.append('/home/chiamin/Projects/mypy')
from CMC_file import *

def read_entropy (fname,STEP=10000,ALL=False):
  if not os.path.isfile (fname):
    print 'Cannot open file:', fname
    exit()
  dat = readprint ('entropy.pl '+fname+' '+str(STEP),typ=float) # x y ind S
  dat = zip(*dat)

  # skip half of sweep
  n = len(dat[0])/2
  xs = dat[0][n:]
  ys = dat[1][n:]
  inds = dat[2][n:]
  Ss = dat[3][n:]

  if ALL == True:
    return xs,ys,inds,Ss
  else:
    Ly = int(max(ys))
    xcol,Scol = [],[]
    for i in xrange(len(xs)):
      if int(ys[i]) == Ly:
        xcol.append (xs[i])
        Scol.append (Ss[i])
    return xcol, Scol

