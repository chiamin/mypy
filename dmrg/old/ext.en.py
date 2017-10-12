import sys
sys.path.append('/home/chiamin/Projects/mypy')
import grace
import numpy as np
from CMC_file import *
import fitfun as ff

gr = grace.new()

def extrap_en (f1,f2):
  V1, trun, en, m, sweep = extra_data (f1)
  V2, trun2, en2, m2, sweep2 = extra_data (f2)
  n = min (len(m), len(m2))

  E = (V2*en2[:n] - V1*en[:n]) / float(V2 - V1)
  Trun = 0.5 * (trun[:n] + trun2[:n])

  fit = ff.polyfit (Trun, E, order=1)
  fitx = np.array([0,max(Trun)])
  fity = ff.polyf (fit, fitx)
  print 'E =', fity[0]

  gr.plot (Trun, E)
  gr.plot (fitx, fity, symb=0)
  grace.show()

def getxy (fname):
  f = open (fname)
  for line in f:
    if 'lx =' in line:
      temp = line.split()
      lx = float(temp[2])
    if 'ly =' in line:
      temp = line.split()
      ly = float(temp[2])
      return lx,ly

def extra_data (fname):
  trun, en, m, sweep = [],[],[],[]
  dat = readprint ('extrapen2.p.test '+fname)
  for di in dat:
    if len(di) == 5:
      try: di = map(float,di)
      except: continue
      trun.append (di[0])
      en.append (di[1])
      m.append (di[3])
      sweep.append (di[4])

  lx,ly = getxy (fname)
  V = lx*ly

  return V, np.array(trun), np.array(en), np.array(m), np.array(sweep)

