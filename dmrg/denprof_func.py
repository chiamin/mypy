import sys
sys.path.append ('/home/chiamin/mypy')
sys.path.append ('/home/chiamin/mypy/dmrg')
from CMC_file import *
from utility import *

# Return re[x,y] = [h,sz]
def store (fname):
  dat = readprint ('spinholeprof.2.pl '+fname, skipline=1) # x y h sz
  re = dict()
  for temp in dat:
    re[(int(temp[0]),int(temp[1]))] = [float(temp[2]),float(temp[3])]
  return re

def bulk_h (x1, x2, dat, Ly):
  Nh = 0.
  for x in xrange(x1,x2+1):
    for y in xrange(1,Ly+1):
      Nh += dat[(x,y)][0]
  nh = Nh / ((x2-x1+1)*Ly)
  return nh

def hx (fname,y=-1):
# if y == -1, average the different y
  lx,ly = getLxy (fname)
  dat = store (fname)

  x = range(1,lx+1)
  n = []
  for xi in x:
    if y == -1:
        n.append (bulk_h (xi,xi,dat,ly))
    else:
        n.append (dat[xi,y][0])
  return x,n

# hsz = [[step,x,y,h,sz],...]
def get_hsz_sweep (fname):
    dat = readprint ('spinholeprof.2.pl '+fname+' -all', skipline=1)
    hsz = []
    for step,x,y,h,sz in dat:
        step,x,y = map(int,[step,x,y])
        h,sz = map(float,[h,sz])
        hsz.append ([step,x,y,h,sz])
    return hsz

# hden = [[step,hole density],..]. step=1,2,3,...
def get_den_sweep (fname):
    dat = readprint ('spinholeprof.2.pl '+fname+' -all', skipline=1)
    maxstep = max(map(int,zip(*dat)[0]))
    den = [[i+1,0.] for i in xrange(maxstep)]
    N = 0
    for step,x,y,h,sz in dat:
        step,x,y = map(int,[step,x,y])
        h,sz = map(float,[h,sz])
        den[step-1][1] += h
        if step == 1: N += 1
    for i in xrange(len(den)):
        den[i][1] = 1.-den[i][1]/N
    return den

# den = [[step,nx],...], where nx is an array
def get_den_x_sweep (fname,y=1):
    dat = readprint ('spinholeprof.2.pl '+fname+' -all', skipline=1)
    maxstep = max(map(int,zip(*dat)[0]))
    den = [[i+1,[]] for i in xrange(maxstep)]
    x = []
    for step,xi,yi,h,sz in dat:
        step,xi,yi = map(int,[step,xi,yi])
        h,sz = map(float,[h,sz])

        if yi == y:
            if step == 1: x.append (xi)
            den[step-1][1].append (1.-h)
    return x, den

def get_den (fname,xmin=1,xmax=10000000):
    dat = readprint ('spinholeprof.2.pl '+fname, skipline=1) # x,y,h,sz
    Nh,N = 0.,0
    for x,y,h,sz in dat:
        x,y,h,sz = int(x),int(y),float(h),float(sz)
        if x >= xmin and x <= xmax:
            Nh += h
            N += 1
    return 1.-Nh/N
