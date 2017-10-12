import sys
sys.path.append('/home/chiamin/Projects/mypy')
import grace
import numpy as np
from CMC_file import *

def get_gmps_overlap (fname):
  f = open(fname)
  for line in f:
    if 'Start measuring...' in line:
      break
  re = []
  for line in f:
    if 'GMPS overlap =' in line:
      re.append (float(line.split()[-1]))
  return re

def geten (fname):
  f = open(fname)
  for line in f:
    if 'Start measuring...' in line:
      break
  re = []
  for line in f:
    if 'E =' in line:
      re.append (float(line.split()[-1]))
  return re

def test():
  gr = grace.new()

  x, sz, szerr, h, herr = hsz_horiz (sys.argv[1],y=1)
  print sz
  gr.errorbar (x,sz,szerr)

  x, sz, szerr, h, herr = hsz_avgY_horiz (sys.argv[1],'even')
  print sz
  gr.errorbar (x,sz,szerr)

  grace.show()

def getLxy (fname):
  f = open (fname)
  for line in f:
    if 'Lx =' in line:
      lx = int(line.split()[-1])
    elif 'Ly =' in line:
      ly = int(line.split()[-1])
      return lx,ly

def file_to_hsz (f):
  for line in f:
    if 'x y sz szerr h herr' in line:
      return

def hsz_horiz (fname,y):
  f = open (fname)
  file_to_hsz (f)

  re = []
  for line in f:
    tmp = map(float,line.split()) # tmp: x y sz szerr h herr szmix szmixerr hmix hmixerr
    if tmp[1] == y:
      re.append ([tmp[0]]+tmp[2:])

  return map(np.array,zip(*re)) # x sz szerr h herr szmix szmixerr hmix hmixerr

def hsz_avgY_horiz (fname,mode='all'):
  lx,ly = getLxy (fname)

  dat = [np.zeros(lx) for i in xrange(4)]
  N = 0
  for y in xrange(1,ly+1):
    #if y==1:
    if mode == 'all'\
    or (mode == 'even' and y%2 == 0)\
    or (mode == 'odd' and y%2 == 1):
      di = hsz_horiz (fname,y)[1:]
      print dat[0]
      print di[0]
      #dat[0] += di[0]
      #print dat[0]
      for i in xrange(len(dat)):
        print i
        dat[i] += di[i]
        print dat[0]
      print '--'
      print dat[0]
      N += 1
  for i in xrange(len(dat)):
    dat[i] /= float(N)

  return [np.arange(1,lx+1)] + dat
