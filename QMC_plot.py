import sys
sys.path.append("/home/bluewhite/Projects/mypy")
from CMC_file import *
from pylab import plot, xlim, ylim

class Diagram_plotter:
  'Plot Diagram'
  diag, hop = [], [];

  def plot_xplane (self, y=0, z=0):
    xplane = self._get_xplane (y, z, self.diag)
    self._plot_xplane (xplane)
    self._plot_xhop (self.hop, y, z)

  def __init__ (self, filename):
    ''' 'diag' should be = [[x, y, t1, t2, ...], ...] '''
    self.diag = readfile (filename.rstrip()+'.line.diag', raw=True)
    self.hop = readfile (filename.rstrip()+'.hop.diag', raw=True)

  def _plot_xhop (self, dat, y, z):
    for xline in dat:
      ''' if xline[0] = 0, 777 or 999: xline[1:] = [x, y, z, t] '''
      ''' else: xline[0] = 1: xline[1:] = [xi, xj, y, z, t] '''
      if xline[0] == 0:
        if (xline[2] == y and xline[3] == z):
          plot (xline[-1], xline[1], color='r', marker='o')
      elif xline[0] == 777 or xline[0] == 999:
        if (xline[2] == y and xline[3] == z):
          plot (xline[-1], xline[1], color='r', marker='s')
      else:
        if (xline[3] == y and xline[4] == z):
          if xline[0] == 1:
            x = [xline[1], xline[2]]
            t = [xline[-1], xline[-1]]
            plot (t, x, color='b', marker='None')
          elif xline[0] == -1:
            x = [xline[1], xline[1]+0.3]
            xx = [xline[2], xline[2]-0.3]
            t = [xline[-1], xline[-1]]
            plot (t, x, color='b', marker='None')
            plot (t, xx, color='b', marker='None')

  def _plot_xplane (self, xplane):
    for xline in xplane: self._plot_xline (xline)

  def _plot_xline (self, line):
    ''' 'line' should be = [x, y, t1, t2, ...] '''
    x = [line[0], line[0]]
    for ti in range(4, len(line)):
      t = [line[ti-1], line[ti]]
      plot (t, x, color='b', marker='o', markersize=4, linestyle=':')

  def _get_xplane (self, y, z, diag):
    xplane = []
    for Wlines in diag:
      if Wlines[1] == float(y) and Wlines[2] == float(z):
        xplane.append(Wlines)
    return xplane


class WLDiagram_plotter (Diagram_plotter):
  'Plot Worldlne diagram'

  def __init__ (self, filename):
    self.diag = readfile (filename.rstrip()+'.line.wld', raw=True)
    self.hop = readfile (filename.rstrip()+'.hop.wld', raw=True)

  def _plot_xline (self, line):
    ''' 'line' should be = [x, y, t1, nbef1, t2, nbef2, ...] '''
    x = [line[0], line[0]]
    for ti in range(4, len(line)-1, 2):
      t = [line[ti-1], line[ti+1]]
      nbef = line[ti+2]
      if nbef == 0:
        plot (t, x, color='b', marker='o', markersize=4, linestyle=':')
      else:
        plot (t, x, color='b', marker='o', markersize=4, linewidth=1+3*(nbef-1))

  def _plot_xplane (self, xplane):
    for xline in xplane: self._plot_xline (xline)
