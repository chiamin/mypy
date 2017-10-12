import sys
sys.path.append ('/home/chiamin/Projects/mypy')
from CMC_file import *

def getLxy (fname):
  f = open (fname)
  for line in f:
    if 'lx =' in line:
      lx = int(line.split()[-1])
    elif 'ly =' in line:
      ly = int(line.split()[-1])
      return lx, ly
  raise KeyError

def getmu (fname):
  f = open (fname)
  for line in f:
    if line == 'hubbard\n': break
  for line in f:
    if 'mu =' in line:
      mu = float(line.split()[-1])
      return mu
  raise KeyError

def getn (fname,sweep=0):
  if sweep == 0:
    dat = readprint ('totN.pl '+fname)
  else:
    dat = readprint ('totN.pl '+fname+' '+str(sweep))
  for line in dat:
    if 'Filling' in line:
      return float(line[-1])
  raise KeyError

def getN (fname,sweep=0):
  if sweep == 0:
    dat = readprint ('totN.pl '+fname)
  else:
    dat = readprint ('totN.pl '+fname+' '+str(sweep))
  for line in dat:
    if line[0]=='Total' and line[1]=='N':
      return float(line[-1])
  raise KeyError

def getbulkn (fname, xfrom, xto, swp=0, hole_or_par='par'):
  if swp == 0:
    dat = readprint ('spinholeprof.2.pl '+fname, skipline=1) # x y h sz
  else:
    dat = readprint ('spinholeprof.2.pl '+fname+' '+str(swp), skipline=1) # x y h sz
  Nsites, htot = 0, 0.
  for di in dat:
    x,y,h,sz = int(di[0]),int(di[1]),float(di[2]),float(di[3])
    if x >= xfrom and x <= xto:
      htot += h
      Nsites += 1
  if hole_or_par == 'par':
    return 1. - htot/Nsites
  else:
    return htot/Nsites

def get_sweeps (fname,mmin=500):
  dat = readprint ('discwt2.p '+fname)
  trun,m,swp = [],[],[]
  mpre = 0
  for di in dat:
    tri,mi,swi = float(di[2]),int(di[3]),int(di[4])
    if mi >= mmin and mi == mpre:
      trun.append (tri)
      m.append (mi)
      swp.append (swi)
    mpre = mi
  return trun, m, swp

# msw[sweep] = m
def get_sweep_m_table (fname):
    dat = readprint ('discwt2.p '+fname)
    msw = dict()
    for trunall, en, trun, m, swp in dat:
        msw[int(swp)] = int(m)
    return msw
