import sys
sys.path.append("/home/bluewhite/Projects/mypy/QMC/")
from QMC_plot import WLDiagram_plotter
from pylab import figure, show, title

def plot (filename, yy):
  f = figure()
  gg = WLDiagram_plotter (filename.rstrip())
  gg.plot_xplane (y=yy)
  title ('y = '+str(yy))
  show()

plot (sys.argv[1], sys.argv[2])
