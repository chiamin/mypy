import sys
sys.path.append ('/home/bluewhite/Projects/mypy')
sys.path.append ('/home/bluewhite/Projects/mypy/QMC')
from CMC_file import *
import pylab as pl
import Statistics as st
import QMC_analysis as aly
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import numpy as np

def nprof (filename, skip=0, T=1):
  rdat = readfile (filename,raw=True)
  Lx, Ly, dat = rdat[0][1], rdat[0][2], zip(*(rdat[1:]))
  means = [T*st.mean(dati[skip:]) for dati in dat]
  if Ly == 1:
    X = range(Lx)
    pl.plot (X, means)
    writefile ('n_profile.dat',[X,means])
  else:
    xis, yis = range(Lx), range(Ly)
    X,Y = np.meshgrid (xis, yis)
    Z = 0.08*np.reshape (means,(Ly,Lx))
    writefile ('n_profile.dat',Z)
    fig = pl.figure ()
    ax = fig.add_subplot (1, 1, 1, projection='3d')
    print X
    print Y
    print Z
    p = ax.plot_surface (X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    pl.figure()
    pl.contour (X,Y,Z)
    pl.colorbar ()
  pl.show()

nprof (sys.argv[1])
