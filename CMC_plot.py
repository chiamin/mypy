from pylab import plot, show, xlabel, ylabel, figure, errorbar, xlim, ylim, xticks, yticks, legend, subplots_adjust, text, title
from scipy import linspace
from matplotlib.ticker import MultipleLocator

class auto_item:
  _item, _ci, _hi, _hold, _x = [], 0, 0, 1, 0
  def __init__ (self,ty='color',h=1):
    self._hold = h
    if ty == 'marker': self._item = ['o','s','^','d','v','<','>']
    elif ty == 'color': self._item = ['b','r','g','k','m','c','orange']
  def l (self): return len(self._item)
  def z (self):
    # call for the item
    self._x = self._item[self._ci]
    self._hi += 1
    if self._hi == self._hold:
      self._hi = 0
      self._ci += 1
    if self._ci == len(self._item): self._ci = 0
    return self._x
  def f (self):
    if self._hold == 1: self._ci, self._hi = 1, 0
    else: self._ci, self._hi = 0, 1
    self._x = self._item[0]
    return self._x
  def reset (self): self._ci, self._hi = 0, 0
  def i (self,i):
    self._x = self._item[i]
    return self._x
  def c (self): return self._x
  def remove (self,x): self._item.remove(x)

def CMC_plot_example():
  x, y, y2, err = [1,2,3], [1,2,3], [0.5, 1, 1.5], [0.1,0.1,0.1]
  f = figure(1)

  # add_subplot (arg1, arg2, arg3):
  #   arg1: number of columns
  #   arg2: number of raws
  #   arg3: which subplot
  ax = f.add_subplot (1,2,1)
  # plot(label) is for legend
  plot (x, y, label='y', marker='o', markersize=6, color='b', markerfacecolor='m', markeredgecolor='b', markeredgewidth=1, linestyle='--', linewidth=1)
  plot (x, y2, label='y2', marker='s', markersize=8, color='r', markerfacecolor='None', markeredgecolor='r', markeredgewidth=2, linestyle=':', linewidth=2)
  # legend(loc): relative location
  # legend(numpoints): number of points
  legend (loc=(0.25,0.75), prop={'size':16}, numpoints=1, frameon=False)
  # xlabel(r'$ ... $') for latex mathbox
  # \mathrm{...} using the normal (non-italic) fonts
  xlabel (r'$ \mathrm{\rho^x} $', fontsize=20)

  # Set the horizontal space
  subplots_adjust (hspace=0.)

  ax2 = f.add_subplot (2,2,2)
  errorbar (x, y, err, marker='^')
  # Doesn't show the xticks
  xticks (visible=False)
  # test(1st and 2nd arguments) set the location on axes
  text (1, 3, '(a)', fontsize=20)

  ax3 = f.add_subplot (2,2,4)
  errorbar (x, y, err, marker='d')
  ylabel ('y2', fontsize=20)
  # Set the major/minor ticks interval for x/y axis
  ax3.xaxis.set_major_locator(MultipleLocator(0.5))
  ax3.xaxis.set_minor_locator(MultipleLocator(0.1))
  ax3.yaxis.set_major_locator(MultipleLocator(0.5))
  ax3.yaxis.set_minor_locator(MultipleLocator(0.1))
  # Show the yticks at right side
  ax3.yaxis.tick_right()
  # Show ylabel at right side
  ax3.yaxis.set_label_position("right")

  show()
#CMC_plot_example()
