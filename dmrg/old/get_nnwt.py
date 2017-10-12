import subprocess as sp
import re, sys

def getdata (filename):
# returned dat: error energy error_per_site m index
  out,err = sp.Popen(['nn.pl',filename], stdout=sp.PIPE).communicate()
  dat = [map(float,di.split()) for di in out.split("\n")]
  dat.remove([])
  return dat

def drop_small_m (dat, mlowerlim=0, mupperlim=sys.maxint):
# return data for only m > mlowerlim
  ndat = []
  istart = 0
  while dat[istart][3] < mlowerlim: istart += 1
  for i in xrange(istart,len(dat)):
    if dat[i][3] <= mupperlim and dat[i][3] == dat[i-1][3] and dat[i][1] != 1e21:
      ndat.append (dat[i])
  return ndat

def nn_and_err (dat):
  dat = map(list,zip(*dat))
  return dat[5], dat[2]

def getLxLyU (filename):
  m = re.search ('(?<=huben)(\d+)(?=x)',filename)
  Lx = int(m.group(0))
  m = re.search ('(?<=x)(\d+)(?=\.)',filename)
  Ly = int(m.group(0))
  m = re.search ('(?<=U)(\d+)(?=\.)',filename)
  U = float(m.group(0))
  return int(Lx),int(Ly),float(U)

