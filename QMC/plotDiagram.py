import sys
sys.path.append("/home/bluewhite/Projects/mypy/QMC/")
from QMC_plot import WLDiagram_plotter
from pylab import figure, show, title, xlabel, ylabel, xlim, ylim

def plot (filename, ax=0, xory=0):
  f = figure()
  gg = WLDiagram_plotter (filename.rstrip())
  print ax, ax==0
  if int(ax) == 0:
    gg.plot_xplane (y=xory)
    title ('y = '+str(xory))
  elif int(ax) == 1:
    gg.plot_yplane (x=xory)
    title ('x = '+str(xory))
  xlabel('time',fontsize=20)
  ylabel('site',fontsize=20)
  #ylim(-2,10)
  show()

plot (sys.argv[1], sys.argv[2], sys.argv[3])
