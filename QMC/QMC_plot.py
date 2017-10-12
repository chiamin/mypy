import sys
sys.path.append("/home/bluewhite/Projects/mypy")
from CMC_file import *
from pylab import plot, xlim, ylim
TIMEL = 1.e8

def valid_time (t):
  return True
  #if t > (TIMEL-1e7) and t < (TIMEL+1e7): return True
  #else: return False

class Diagram_plotter:
  'Plot Diagram'
  diag, hop = [], [];

  def plot_xplane (self, y=0, z=0):
    xplane = self._get_xplane (y, z, self.diag)
    self._plot_plane (xplane, ax=0)
    self._plot_xhop (self.hop, y, z)
  def plot_yplane (self, x=0, z=0):
    yplane = self._get_yplane (x, z, self.diag)
    self._plot_plane (yplane, ax=1)
    self._plot_yhop (self.hop, x, z)

  def __init__ (self, filename):
    ''' 'diag' should be = [[x, y, t1, t2, ...], ...] '''
    self.diag = readfile (filename.rstrip()+'.line.diag', raw=True)
    self.hop = readfile (filename.rstrip()+'.hop.diag', raw=True)

  def _plot_xhop (self, dat, y, z):
    inty = int(y)
    for line in dat:
      ''' if line[0] = 0, 777 or 999: line[1:] = [x, y, z, t] '''
      ''' else: line[0] = 1: line[1:] = [xi, xj, y, z, t] '''
      if line[0] == 0:
        if (line[2] == y and line[3] == z):
          if valid_time(line[-1]): plot (line[-1], line[1], color='r', marker='o')
      elif line[0] == 777 or line[0] == 999:
        if (line[2] == y and line[3] == z):
          if valid_time(line[-1]): plot (line[-1], line[1], color='r', marker='s')
      else:
        if (line[3] == inty and line[4] == z):
          if line[0] == 1:
            x = [line[1], line[2]]
            t = [line[-1], line[-1]]
            if valid_time(t[0]): plot (t, x, color='b', marker='None')
          elif line[0] == -1:
            x = [line[1], line[1]+0.3]
            xx = [line[2], line[2]-0.3]
            t = [line[-1], line[-1]]
            if valid_time(t[0]): plot (t, x, color='b', marker='None')
            if valid_time(t[0]): plot (t, xx, color='b', marker='None')

  def _plot_yhop (self, dat, x, z):
    intx = int(x)
    for line in dat:
      ''' if line[0] = 0, 777 or 999: line[1:] = [x, y, z, t] '''
      ''' else: line[0] = 2: line[1:] = [yi, yj, x, z, t] '''
      if line[0] == 0:
        if (line[1] == x and line[3] == z):
          if valid_time(line[-1]): plot (line[-1], line[0], color='r', marker='o')
      elif line[0] == 777 or line[0] == 999:
        if (line[1] == x and line[3] == z):
          if valid_time(line[-1]): plot (line[-1], line[0], color='r', marker='s')
      else:
        if line[3] == intx and line[4] == z:
          if line[0] == 2:
            x = [line[1], line[2]]
            t = [line[-1], line[-1]]
            if valid_time(t[0]): plot (t, x, color='b', marker='None')
          elif line[0] == -2:
            x = [line[1], line[1]+0.3]
            xx = [line[2], line[2]-0.3]
            t = [line[-1], line[-1]]
            if valid_time(t[0]): plot (t, x, color='b', marker='None')
            if valid_time(t[0]): plot (t, xx, color='b', marker='None')

  def _plot_plane (self, plane, ax=0):
    for line in plane: self._plot_line (line, ax)

  def _plot_line (self, line, ax=0):
    ''' 'line' should be = [x, y, t1, t2, ...] '''
    x = [line[ax], line[ax]]
    for ti in range(4, len(line)):
      t = [line[ti-1], line[ti]]
      plot (t, x, color='b', marker='o', markersize=4, linestyle=':')

  def _get_xplane (self, y, z, diag):
    xplane = []
    for Wlines in diag:
      if Wlines[1] == float(y) and Wlines[2] == float(z):
        xplane.append(Wlines)
    return xplane

  def _get_yplane (self, x, z, diag):
    plane = []
    for Wlines in diag:
      if Wlines[0] == float(x) and Wlines[2] == float(z):
        plane.append(Wlines)
    return plane


class WLDiagram_plotter (Diagram_plotter):
  'Plot Worldlne diagram'

  def __init__ (self, filename):
    self.diag = readfile (filename.rstrip()+'.line.wld', raw=True)
    self.hop = readfile (filename.rstrip()+'.hop.wld', raw=True)

  def _plot_line (self, line, ax=0):
    ''' 'line' should be = [x, y, t1, nbef1, t2, nbef2, ...] '''
    x = [line[ax], line[ax]]
    for ti in range(4, len(line)-1, 2):
      if valid_time (line[ti-1]):
        t = [line[ti-1], line[ti+1]]
        nbef = line[ti+2]
        if nbef == 0:
          plot (t, x, color='b', marker='o', markersize=4, linestyle=':')
        else:
          plot (t, x, color='b', marker='o', markersize=4, linewidth=1+3*(nbef-1))

  def _plot_plane (self, xplane, ax=0):
    for line in xplane: self._plot_line (line,ax)
