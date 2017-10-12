import pylab as pl
import sys
import Dator as dt

FILE = sys.argv[1]
obs = sys.argv[2]
def plot_corrtime (FILE, obs):
  dt.read (FILE)
  ks, corrtime = dt.get (obs+'_binsize'), dt.get (obs+'_corrtime')
  #pl.figure()
  print ks
  pl.plot (ks, corrtime, label=obs)
  pl.xlabel ('bin size', fontsize=20)
  pl.ylabel ('ACT', fontsize=20)
#plot_corrtime (FILE, 'close_weight')
#plot_corrtime (FILE, 'open_weight')
#plot_corrtime (FILE, 'switch_prob')
plot_corrtime (FILE, obs)
pl.legend()
pl.show()
