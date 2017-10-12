import sys
sys.path.append('/home/chiamin/Projects/mypy')
sys.path.append('/home/chiamin/Projects/mypy/cpmc')
import grace
import numpy as np
import fitfun as ff
import cpmc_ana as ca

def main():
  fname = sys.argv[1]
  m,trun,en = geten (sys.argv[1])
  lx,ly = ca.getLxy (fname)
  V = lx*ly
  print 'm =',m,'\ntrun =',trun,'\nen =',np.array(en)/V
  plot_ext_en (trun,en)

def geten (fname):
  f = open (fname)
  for line in f:
    if 'Making input group basic.sweeps' in line:
      #temp = line.split()
      #temp = temp[-1].lstrip('basic.sweeps')
      #sweepi = int(temp)
      break

  en,m,trun = [],[],[]
  for line in f:
    if 'Largest m' in line:
      temp = line.split()
      mtemp = int(temp[-1])
    if 'Largest truncation' in line:
      temp = line.split()
      ttemp = float(temp[-1])
    if 'Energy after' in line:
      temp = line.split()
      etemp = float(temp[-1])

    if 'Making input group basic.sweeps' in line or 'Up density' in line:
      m.append (mtemp)
      trun.append (ttemp)
      en.append (etemp)

  return m,trun,en


def plot_ext_en (trun,en):
  gr = grace.new()
  gr.plot (trun,en)
  grace.show()

main()
