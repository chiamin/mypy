from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import pylab as pl

def plot_latt_obs (Lx,Ly,dat):
  dat = np.array(dat)
  dat = np.reshape (dat,(Lx,Ly))
  x,y = np.meshgrid (range(Lx),range(Ly))
  ax = pl.gca (projection='3d')
  #ax.plot_surface (x,y,dat, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
  ax.plot_wireframe (x,y,dat, rstride=2, cstride=2)

