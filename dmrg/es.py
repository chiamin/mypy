import sys
sys.path.append ('/home/chiamin/Projects/mypy')
sys.path.append ('/home/chiamin/Projects/mypy/dmrg')
import grace
import numpy as np
import utility as ut

gr = grace.new()

def extract (line):
  tmp = line.split()
  sz = int(tmp[0].lstrip('Sz='))
  N  = int(tmp[1].lstrip('N='))
  w  = float(tmp[2])
  i  = int(tmp[3])
  return sz, N, w, i

def read_weight (fname):
  lx,ly = ut.getLxy (fname)
  x,y = lx/2,ly
  if len(sys.argv) >= 3:
    x,y = sys.argv[2], sys.argv[3]
  print 'x,y =',x,y

  # Get the block
  f = open (fname).readlines()
  it = -1
  for i in xrange(len(f)-1,-1,-1):
    it, line = i, f[i]
    key = 'x=('+str(x)+','+str(y)+')'
    if key in line:
      break
  f = f[it:]

  for i in xrange(len(f)):
    it, line = i, f[i]
    if 'Weight in' in line:
      break
  f = f[it+1:]

  # Get weights
  dat = []
  for line in f:
    if 'BlockMat' in line: break
    tmp = line.rstrip('\n').split('\t')
    if len(tmp) == 2:
      tmp = tmp[-1].split()
      if 'Sz' not in tmp[0]: break
      sz   = int(tmp[0].strip('Sz=,'))
      N    = int(tmp[1].lstrip('N='))
      wsum = float(tmp[2])
      Nw   = int(tmp[3])
    elif len(tmp) == 3:
      tmp = tmp[-1].split()
      w = float(tmp[-1])
      dat.append ([sz,N,w])
  return np.array(zip(*dat)) # sz,N,w

sz,N,w = read_weight (sys.argv[1])
gr.plot (N+0.1*sz,-np.log(w**2),ls=0)
grace.show()
