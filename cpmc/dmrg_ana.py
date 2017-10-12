import sys
sys.path.append('/home/chiamin/Projects/mypy')
import grace
import numpy as np
from CMC_file import *

def main():
  #test()
  pass

def test():
  gr = grace.new()

  x, sz, h = hsz_horiz (sys.argv[1],y=1)
  gr.plot (x,sz)

  x, sz, h = hsz_avgY_horiz (sys.argv[1],'odd')
  gr.plot (x,sz)

  grace.show()

def getLxy (fname):
  f = open (fname)
  for line in f:
    if '** ?	?	Lx	Ly	maxsz	maxh **' in line:
      break
  for line in f:
    tmp = line.split()
    return int(tmp[2]), int(tmp[3])

def file_to_hsz (f):
  for line in f:
    if '**   x   y   sz   h **' in line:
      return

def hsz_horiz (fname,y):
  f = open (fname)
  file_to_hsz (f)

  re = []
  for line in f:
    tmp = map(float,line.split()) # tmp: x   y   sz   h
    if tmp[1] == y:
      re.append ([tmp[0]]+tmp[2:])

  return map(np.array,zip(*re)) # x   y   sz   h

def hsz_avgY_horiz (fname,mode='all'):
  lx,ly = getLxy (fname)

  dat = [np.zeros(lx) for i in xrange(2)]
  N = 0
  for y in xrange(1,ly+1):
    #if y==1:
    if mode == 'all'\
    or (mode == 'even' and y%2 == 0)\
    or (mode == 'odd' and y%2 == 1):
      di = hsz_horiz (fname,y)[1:]
      for i in xrange(len(dat)):
        dat[i] += di[i]
      N += 1
  for i in xrange(len(dat)):
    dat[i] /= float(N)

  return [np.arange(1,lx+1)] + dat
    

main()
