import os

GRAPHS = []
GI = 0

# ================ Graph class ====================
class Graph:
  def __init__(self, graph_i=0):
    self.i = 0
    self.batch = []
    self.xmdat = []
    self.Ncolors = 11
    self.Nsymbols = 11
    self.Gi = graph_i
    self.dfile = '.temp.dat.'+str(self.Gi)
    self.bfile = '.temp.batch.'+str(self.Gi)
    self.named = False
    self.flag = ''
    self.pset = False
    self.used_color = []
    self.used_symbol = []

  def special_char (self,string):
    string = string.replace ("\\alpha","\\x a\\f{}")
    string = string.replace ("\\beta","\\x b\\f{}")
    string = string.replace ("\\chi","\\x c\\f{}")
    string = string.replace ("\\delta","\\x d\\f{}")
    string = string.replace ("\\epsilon","\\x e\\f{}")
    string = string.replace ("\\phi","\\x f\\f{}")
    string = string.replace ("\\gamma","\\x g\\f{}")
    string = string.replace ("\\eta","\\x h\\f{}")
    string = string.replace ("\\iota","\\x i\\f{}")
    string = string.replace ("\\varphi","\\x j\\f{}")
    string = string.replace ("\\kappa","\\x k\\f{}")
    string = string.replace ("\\lambda","\\x l\\f{}")
    string = string.replace ("\\mu","\\x m\\f{}")
    string = string.replace ("\\nu","\\x n\\f{}")
    string = string.replace ("\\pi","\\x p\\f{}")
    string = string.replace ("\\theta","\\x q\\f{}")
    string = string.replace ("\\rho","\\x r\\f{}")
    string = string.replace ("\\sigma","\\x s\\f{}")
    string = string.replace ("\\tau","\\x t\\f{}")
    string = string.replace ("\\upsilon","\\x u\\f{}")
    string = string.replace ("\\varpi","\\x v\\f{}")
    string = string.replace ("\\omega","\\x w\\f{}")
    string = string.replace ("\\xi","\\x x\\f{}")
    string = string.replace ("\\psi","\\x y\\f{}")
    string = string.replace ("\\zeta","\\x z\\f{}")
    string = string.replace ("\\Delta","\\x D\\f{}")
    string = string.replace ("\\Phi","\\x F\\f{}")
    string = string.replace ("\\Gamma","\\x G\\f{}")
    string = string.replace ("\\vartheta","\\x J\\f{}")
    string = string.replace ("\\Pi","\\x P\\f{}")
    string = string.replace ("\\Theta","\\x Q\\f{}")
    string = string.replace ("\\Sigma","\\x S\\f{}")
    string = string.replace ("\\varsigma","\\x V\\f{}")
    string = string.replace ("\\Omega","\\x W\\f{}")
    string = string.replace ("\\Xi","\\x X\\f{}")
    string = string.replace ("\\Psi","\\x Y\\f{}")
    string = string.replace ("\\langle","\\x\\ca\\C\\f{}")
    string = string.replace ("\\rangle","\\x\\cq\\C\\f{}")
    string = string.replace ("\\infty","\\x\\c%\\C\\f{}")
    string = string.replace ("\\Rightarrow","\\x\\c^\\C\\f{}")
    string = string.replace ("\\to","\\x\\c.\\C\\f{}")
    string = string.replace ("\\pm","\\x\\c1\\C\\f{}")
    string = string.replace ("\\geq","\\x\\c3\\C\\f{}")
    string = string.replace ("\\partial","\\x\\c6\\C\\f{}")
    string = string.replace ("\\neq","\\x\\c9\\C\\f{}")
    string = string.replace ("\\sum","\\x\\ce\\C\\f{}")
    string = string.replace ("\\int","\\x\\cr\\C\\f{}")
    string = string.replace ("\\nabla","\\x\\cQ\\C\\f{}")
    string = string.replace ("\\prod","\\x\\cU\\C\\f{}")
    string = string.replace ("\\approx","\\x\\c;\\C\\f{}")
    string = string.replace ("\\leq","\\x\\c#\\C\\f{}")
    string = string.replace ("\\in","\\x\\cN\\C\\f{}")
    string = string.replace ("\\forall","\\x\"\\C\\f{}")
    string = string.replace ("\\dagger","\\f{ZapfDingbats}=\\f{}")
    string = string.replace ("\\times","\\x\\c4\\C\\f{}")

    def replace_pair (string, left, right, left2, right2):

      def replace_one (string, old, new, beg=0, end=-1):
         if end == -1:
            return string[:beg] + string[beg:].replace (old,new,1)
         else:
            return string[:beg] + string[beg:end].replace (old,new,1) + string[end:]

      def replace_next (string, old, new, beg):
         loc = string.find (old, beg)
         if loc == -1: return string, -1
         string = replace_one (string, old, new, loc)
         return string, loc

      beg = 0
      while True:
        string, beg = replace_next (string, left, left2, beg)
        if beg == -1: break
        string, beg = replace_next (string, right, right2, beg)
        if beg == -1:
          print 'grace.py: special_char: cannot find matched pair: ',left,right
          raise

      return string

    string = replace_pair (string, '^{','}','\\S','\\N')
    string = replace_pair (string, '_{','}','\\s','\\N')
    return string

  def filename (self,name):
    self.dfile = name+'.agr'
    self.named = True

  def write (self):
    self.colordef()

    f = open (self.bfile,'w')
    for line in self.batch: f.write (line)
    f.close()

    f = open (self.dfile,'w')
    for line in self.xmdat: f.write (line)
    f.close()

  def clear (self):
    self.i = 0
    self.xmdat = []
    self.batch = []
    self.pset = False
    self.used_color = []
    self.used_symbol = []
    # Remove temporary files
    os.system ('rm '+self.bfile)
    if not self.named:
      os.system ('rm '+self.dfile)

  def auto_color (self):
    if len(self.used_color) == self.Ncolors:
      self.used_color = []
    for i in xrange(1,self.Ncolors+1):
      if i not in self.used_color:
        self.used_color.append (i)
        return i
    print 'Error: color not found'
    raise

  def auto_symb (self):
    if len(self.used_symbol) == self.Nsymbols:
      self.used_symbol = []
    for i in xrange(1,self.Nsymbols+1):
      if i not in self.used_symbol:
        self.used_symbol.append (i)
        return i
    print 'Error: symbol not found'
    raise

  def get_color (self,c):
    if c == 'auto': c = self.auto_color()
    elif c == 'same': c = self.used_color[-1]
    elif c == 'k': c = 1
    elif c == 'r': c = 2
    elif c == 'b': c = 3
    elif c == 'g': c = 4
    return c

  def get_symbol (self,symb):
    if symb == 'auto': symb = self.auto_symb()
    elif symb == 'same': symb = self.used_symbol[-1]
    elif symb == 'o': symb = 1
    elif symb == 's': symb = 2
    elif symb == 'd': symb = 3
    elif symb == '^': symb = 4
    elif symb == '+': symb = 8
    elif symb == 'x': symb = 9
    return symb

  def general_plot_batch (self,c='auto',symb='auto',symbfill='0',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,legend=''):
    # c: Color
    # symb: Symbol
    # ls: Line style
    # lw: Line width
    # symbsz: Symbol size
    # symblw: Symbol line width
    # symbfill: Symbol fill pattern
    # legend: Legend
    legend = self.special_char (legend)

    c = self.get_color (c)
    if int(c) not in self.used_color:
     self.used_color.append(int(c))

    symb = self.get_symbol (symb)
    if int(symb) not in self.used_symbol:
     self.used_symbol.append(int(symb))

    if ls == '--': ls = '4'
    elif ls == '-': ls = '1'
    elif ls == '..': ls = '2'

    self.batch.append ('s'+str(self.i)+' linestyle '+str(ls)+'\n')
    self.batch.append ('s'+str(self.i)+' linewidth '+str(lw)+'\n')
    self.batch.append ('s'+str(self.i)+' color '+str(c)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol '+str(symb)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol color '+str(c)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol size '+str(symbsz)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol linewidth '+str(symblw)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol fill pattern '+str(symbfill)+'\n')
    self.batch.append ('s'+str(self.i)+' symbol fill color '+str(c)+'\n')
    self.batch.append ('s'+str(self.i)+' legend "'+legend+'"\n')

  def plot (self,x,y,c='auto',symb='auto',symbfill='0',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,legend=''):
    for xi,yi in zip(x,y):
      self.xmdat.append (str(xi)+' '+str(yi)+' 0\n')
    self.xmdat.append ('\n')

    self.batch.append ('s'+str(self.i)+' type xy\n')
    self.general_plot_batch (c=c,symb=symb,symbfill=symbfill,ls=ls,lw=lw,symbsz=symbsz,symblw=symblw,legend=legend)

    self.i += 1


  def errorbar (self,x,y,e,c='auto',symb='auto',symbfill='0',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,errlw=1.0,legend=''):

    for j in xrange(len(x)):
      self.xmdat.append (str(x[j])+' '+str(y[j])+' '+str(e[j])+'\n')
    self.xmdat.append ('\n')

    c = self.get_color (c)
    if int(c) not in self.used_color:
     self.used_color.append(int(c))

    symb = self.get_symbol (symb)
    if int(symb) not in self.used_symbol:
     self.used_symbol.append(int(symb))

    self.batch.append ('s'+str(self.i)+' type xydy\n')
    self.general_plot_batch (c=c,symb=symb,symbfill=symbfill,ls=ls,lw=lw,symbsz=symbsz,symblw=symblw,legend=legend)
    self.batch.append ('s'+str(self.i)+' errorbar color '+str(c)+'\n')
    self.batch.append ('s'+str(self.i)+' errorbar linewidth '+str(errlw)+'\n')

    self.i += 1


  def text (self,x,y,text,dx=0,dy=0,c='1',size=1):
    if c == 'same': c = self.used_color[-1]
    self.batch.append ('\nwith string\n')
    self.batch.append ('string on\n')
    self.batch.append ('string loctype world\n')
    self.batch.append ('string color '+str(c)+'\n')
    self.batch.append ('string char size '+str(size)+'\n')
    self.batch.append ('string '+str(x+dx)+', '+str(y+dy)+'\n')
    self.batch.append ('string def "'+str(text)+'"\n')

  def texts (self,xs,ys,ts,dx=0,dy=0,c='1',size=1):
    for i in xrange(len(xs)):
      self.text (xs[i],ys[i],ts[i],dx,dy,c,size)

  def setp (self,title='',xlabel='',ylabel='',xscale='NORMAL',yscale='NORMAL'\
           ,xinv=0, yinv=0\
           ,leg=True,legx=0.2,legy=0.8,legsz=1.0,legvgap=1.0\
           ,xlabsz=1.0,ylabsz=1.0,xbarlw=1.0,ybarlw=1.0\
           ,xticklab=True,yticklab=True,xticksz=1.0,yticksz=1.0\
           ,xtickmaj='auto',ytickmaj='auto',xtickms='auto',ytickms='auto',xlabc='1',ylabc='1'\
           ,xlabopp=0,ylabopp=0,xtickside='both',ytickside='both',xside='',yside=''\
           ):
    # title: Title
    # xlabel: x-axis label
    # ylabel: y-axis label
    # xscale: x-axis scale, can be 'Normal' or 'log'(Logarithmic)
    # yscale: y-axis scale, can be 'Normal' or 'log'(Logarithmic)
    # legx: Legend positoin in x-axis
    # legy: Legend positoin in y-axis
    # legsz: Legend size
    # xlabsz: x-axis label size
    # ylabsz: y-axis label size
    # xbarlw: x-bar line width
    # ybarlw: y-bar line width
    # xticksz: x-axis tick font size
    # yticksz: y-axis tick font size
    #if xscale == 'log': xscale = 'LOGARITHMIC'
    #if yscale == 'log': yscale = 'LOGARITHMIC'
    # xtickside: can be 'both', 'up(u)', or 'down'('d')
    # ytickside: can be 'both', 'left(l)', or 'right(r)'
    title = self.special_char (title)
    xlabel = self.special_char (xlabel)
    ylabel = self.special_char (ylabel)
    if xscale == 'log' and yscale == 'log': self.flag += ' -log xy'
    elif xscale == 'log': self.flag += ' -log x'
    elif yscale == 'log': self.flag += ' -log y'
    if leg: leg = 'on'
    else: leg = 'off'
    if xticklab: xticklab = 'on'
    else: xticklab = 'off'
    if yticklab: yticklab = 'on'
    else: yticklab = 'off'

    dict_xtickside = {'both':'both', 'down':'normal', 'up':'opposite', 'd':'normal', 'u':'opposite'}
    xtickside = dict_xtickside [xtickside]
    dict_ytickside = {'both':'both', 'left':'normal', 'right':'opposite', 'l':'normal', 'r':'opposite'}
    ytickside = dict_ytickside [ytickside]

    if xside == 'down' or xside == 'd':
       xlabopp = 0
       xtickside = 'normal'
    elif xside == 'up' or xside == 'u':
       xlabopp = 1
       xtickside = 'opposite'
    if yside == 'left' or yside == 'l':
       ylabopp = 0
       ytickside = 'normal'
    elif yside == 'right' or yside == 'r':
       ylabopp = 1
       ytickside = 'opposite'


    self.batch.append ('title "'+title+'"\n')
    self.batch.append ('xaxis label "'+xlabel+'"\n')
    self.batch.append ('yaxis label "'+ylabel+'"\n')
    #self.batch.append ('xaxes scale '+xscale+'\n')
    #self.batch.append ('yaxes scale '+yscale+'\n')
    self.batch.append ('xaxis label char size '+str(xlabsz)+'\n')
    self.batch.append ('yaxis label char size '+str(ylabsz)+'\n')
    self.batch.append ('xaxis bar linewidth '+str(xbarlw)+'\n')
    self.batch.append ('yaxis bar linewidth '+str(ybarlw)+'\n')
    self.batch.append ('legend '+leg+'\n')
    self.batch.append ('legend '+str(legx)+', '+str(legy)+'\n')
    self.batch.append ('legend char size '+str(legsz)+'\n')
    self.batch.append ('legend vgap '+str(legvgap)+'\n')
    self.batch.append ('xaxis ticklabel '+xticklab+'\n')
    self.batch.append ('yaxis ticklabel '+yticklab+'\n')
    self.batch.append ('xaxis ticklabel char size '+str(xticksz)+'\n')
    self.batch.append ('yaxis ticklabel char size '+str(yticksz)+'\n')
    if xtickmaj != 'auto': self.batch.append ('xaxis tick major '+str(xtickmaj)+'\n')
    if ytickmaj != 'auto': self.batch.append ('yaxis tick major '+str(ytickmaj)+'\n')
    if xtickms != 'auto': self.batch.append ('xaxis tick minor ticks '+str(xtickms)+'\n')
    if ytickms != 'auto': self.batch.append ('yaxis tick minor ticks '+str(ytickms)+'\n')
    self.batch.append ('xaxis ticklabel color '+str(xlabc)+'\n')
    self.batch.append ('yaxis ticklabel color '+str(ylabc)+'\n')
    self.batch.append ('xaxis label color '+str(xlabc)+'\n')
    self.batch.append ('yaxis label color '+str(ylabc)+'\n')
    if xlabopp:
       self.batch.append ('xaxis ticklabel place opposite\n')
       self.batch.append ('xaxis label place opposite\n')
    if ylabopp:
       self.batch.append ('yaxis ticklabel place opposite\n')
       self.batch.append ('yaxis label place opposite\n')
    self.batch.append ('xaxis tick place '+str(xtickside)+'\n')
    self.batch.append ('yaxis tick place '+str(ytickside)+'\n')
    self.pset = True
    if xinv: self.batch.append ('xaxes invert on\n')
    if yinv: self.batch.append ('yaxes invert on\n')

  def view (self,xmin=0.15,ymin=0.15,xmax=1.15,ymax=0.85):
    self.flag += ' -viewport '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)

  def pagesize (self,xsize=792,ysize=612):
    self.flag += ' -fixed '+str(xsize)+' '+str(ysize)

  def colordef (self):
    # Define auto color here
    self.batch.append ('map color 0 to (255, 255, 255), "white"\n')
    self.batch.append ('map color 1 to (0, 0, 0), "black"\n')
    self.batch.append ('map color 2 to (255, 0, 0), "red"\n')
    self.batch.append ('map color 3 to (0, 0, 255), "blue"\n')
    self.batch.append ('map color 4 to (0, 139, 0), "green4"\n')
    self.batch.append ('map color 5 to (255, 128, 0), "orange"\n')
    self.batch.append ('map color 6 to (255, 0, 255), "magenta"\n')
    self.batch.append ('map color 7 to (166, 86, 40), "brown"\n')
    self.batch.append ('map color 8 to (103, 7, 72), "maroon"\n')
    self.batch.append ('map color 9 to (102, 0, 204), "purple"\n')
    self.batch.append ('map color 10 to (0, 102, 51), "green"\n')
    self.batch.append ('map color 11 to (64, 224, 208), "turquoise"\n')
    self.batch.append ('map color 12 to (166, 206, 227), "lightblue"\n')
    self.batch.append ('map color 13 to (178, 223, 138), "lightgreen"\n')
    self.batch.append ('map color 14 to (251, 154, 153), "lightred"\n')
    self.batch.append ('map color 15 to (253, 191, 111), "lightorange"\n')

  # ----------------  User-defined settings  -------------------
  def paperset (self,lw = 2,symbsz = 1.4,symblw = 2,errlw = 2,legsz = 1.2\
                 ,legvgap=2,xlabsz=1.4,ylabsz=1.4,xbarlw=2,ybarlw=2,xticksz=1.4,yticksz=1.4):
    if not self.pset: self.setp()
    ilw = iss = islw = ielw = 0
    for i in xrange(len(self.batch)):
      if 's'+str(ilw)+' linewidth ' in self.batch[i]:
        self.batch[i] = 's'+str(ilw)+' linewidth '+str(lw)+'\n'
        ilw += 1
      elif 's'+str(iss)+' symbol size ' in self.batch[i]:
        self.batch[i] = 's'+str(iss)+' symbol size '+str(symbsz)+'\n'
        iss += 1
      elif 's'+str(islw)+' symbol linewidth ' in self.batch[i]:
        self.batch[i] = 's'+str(islw)+' symbol linewidth '+str(symblw)+'\n'
        islw += 1
      elif 's'+str(ielw)+' errorbar linewidth ' in self.batch[i]:
        self.batch[i] = 's'+str(ielw)+' errorbar linewidth '+str(errlw)+'\n'
        ielw += 1
      elif 'legend char size ' in self.batch[i]:
        self.batch[i] = 'legend char size '+str(legsz)+'\n'
      elif 'legend vgap ' in self.batch[i]:
        self.batch[i] = 'legend vgap '+str(legvgap)+'\n'
      elif 'xaxis label char size ' in self.batch[i]:
        self.batch[i] = 'xaxis label char size '+str(xlabsz)+'\n'
      elif 'yaxis label char size ' in self.batch[i]:
        self.batch[i] = 'yaxis label char size '+str(ylabsz)+'\n'
      elif 'xaxis bar linewidth ' in self.batch[i]:
        self.batch[i] = 'xaxis bar linewidth '+str(xbarlw)+'\n'
      elif 'yaxis bar linewidth ' in self.batch[i]:
        self.batch[i] = 'yaxis bar linewidth '+str(ybarlw)+'\n'
      elif 'xaxis ticklabel char size ' in self.batch[i]:
        self.batch[i] = 'xaxis ticklabel char size '+str(xticksz)+'\n'
      elif 'yaxis ticklabel char size ' in self.batch[i]:
        self.batch[i] = 'yaxis ticklabel char size '+str(yticksz)+'\n'
  #----------------- User-defined settings ----------------------

# ================ End of Graph class ====================

# ================ Global functions ==================

def showg (graphs,name=''):

  #if name != '':
  #  graphs[-1].filename (name)

  command = ''
  for gi in graphs:
    gi.write()
    command += ' -graph '+str(gi.Gi)+' -type xydy -autoscale xy '+gi.dfile+' -nosafe -param '+gi.bfile+gi.flag

  print command
  os.system ('xmgrace '+command)

  for gi in graphs:
    gi.clear()


def new ():
  global GRAPHS
  global GI
  GRAPHS.append (Graph (GI))
  GI += 1
  return GRAPHS[-1]

def show (name=''):
  global GRAPHS
  global GI
  showg (GRAPHS,name)

def clean ():
  global GRAPHS
  global GI
  GI = 0
  GRAPHS = []

