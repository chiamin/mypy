import os

i = 0
batch = []
xmdat = []
auto_color = ['1','2','3','4','5','6','7','8','9','10','11']#,'12','13','14','15']
auto_symbol = ['1','2','3','4','5','6','7','8','9','10','11']
Gi = 0 # graph number

# ===================  User-defined settings  ===========================
def paper_plot (lw = 2,symbsz = 2,symblw = 2,errlw = 2,legsz = 1.2,xlabsz=2,ylabsz=2,xbarlw=2,ybarlw=2,xticksz=1.75,yticksz=1.75):
  global batch

  ilw = iss = islw = ielw = 0
  for i in xrange(len(batch)):
    if 's'+str(ilw)+' linewidth ' in batch[i]:
      batch[i] = 's'+str(ilw)+' linewidth '+str(lw)+'\n'
      ilw += 1
    elif 's'+str(iss)+' symbol size ' in batch[i]:
      batch[i] = 's'+str(iss)+' symbol size '+str(symbsz)+'\n'
      iss += 1
    elif 's'+str(islw)+' symbol linewidth ' in batch[i]:
      batch[i] = 's'+str(islw)+' symbol linewidth '+str(symblw)+'\sn'
      islw += 1
    elif 's'+str(ielw)+' errorbar linewidth ' in batch[i]:
      batch[i] = 's'+str(ielw)+' errorbar linewidth '+str(errlw)+'\n'
      ielw += 1
    elif 'legend char size ' in batch[i]:
      batch[i] = 'legend char size '+str(legsz)+'\n'
    elif 'xaxis label char size ' in batch[i]:
      batch[i] = 'xaxis label char size '+str(xlabsz)+'\n'
    elif 'yaxis label char size ' in batch[i]:
      batch[i] = 'yaxis label char size '+str(ylabsz)+'\n'
    elif 'xaxis bar linewidth ' in batch[i]:
      batch[i] = 'xaxis bar linewidth '+str(xbarlw)+'\n'
    elif 'yaxis bar linewidth ' in batch[i]:
      batch[i] = 'yaxis bar linewidth '+str(ybarlw)+'\n'
    elif 'xaxis ticklabel char size ' in batch[i]:
      batch[i] = 'xaxis ticklabel char size '+str(xticksz)+'\n'
    elif 'yaxis ticklabel char size ' in batch[i]:
      batch[i] = 'yaxis ticklabel char size '+str(yticksz)+'\n'
#=======================================================================


def color (j=0):
  global i
  return auto_color  [(i+j)%len(auto_color)]

def symb (j=0):
  global i
  return auto_symbol [(i+j)%len(auto_color)]

def general_plot_batch (c='auto',symb='auto',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,legend=''):
  # c: Color
  # symb: Symbol
  # ls: Line style
  # lw: Line width
  # symbsz: Symbol size
  # symblw: Symbol line width
  # legend: Legend
  global batch
  batch.append ('s'+str(i)+' linestyle '+ls+'\n')
  batch.append ('s'+str(i)+' linewidth '+str(lw)+'\n')
  batch.append ('s'+str(i)+' color '+c+'\n')
  batch.append ('s'+str(i)+' symbol '+symb+'\n')
  batch.append ('s'+str(i)+' symbol color '+c+'\n')
  batch.append ('s'+str(i)+' symbol size '+str(symbsz)+'\n')
  batch.append ('s'+str(i)+' symbol linewidth '+str(symblw)+'\n')
  batch.append ('s'+str(i)+' legend "'+legend+'"\n')

def plot (x,y,c='auto',symb='auto',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,legend=''):
  global i
  global batch

  for xi,yi in zip(x,y):
    xmdat.append (str(xi)+' '+str(yi)+' 0\n')
  xmdat.append ('\n')

  if c == 'auto': c = auto_color [i%len(auto_color)]
  if symb == 'auto': symb = auto_symbol [i%len(auto_symbol)]

  batch.append ('s'+str(i)+' type xy\n')
  general_plot_batch (c=c,symb=symb,ls=ls,lw=lw,symbsz=symbsz,symblw=symblw,legend=legend)

  i += 1


def errorbar (x,y,e,c='auto',symb='auto',ls='1',lw=1.0,symbsz=1.0,symblw=1.0,errlw=1.0,legend=''):
  global i
  global batch

  for j in xrange(len(x)):
    xmdat.append (str(x[j])+' '+str(y[j])+' '+str(e[j])+'\n')
  xmdat.append ('\n')

  if c == 'auto': c = auto_color [i%len(auto_color)]
  if symb == 'auto': symb = auto_symbol [i%len(auto_symbol)]

  batch.append ('s'+str(i)+' type xydy\n')
  general_plot_batch (c=c,symb=symb,ls=ls,lw=lw,symbsz=symbsz,symblw=symblw,legend=legend)
  batch.append ('s'+str(i)+' errorbar color '+c+'\n')
  batch.append ('s'+str(i)+' errorbar linewidth '+str(errlw)+'\n')

  i += 1


def text (x,y,text,dx=0,dy=0,c='1',size=1):
  global batch
  batch.append ('\nwith string\n')
  batch.append ('string on\n')
  batch.append ('string loctype world\n')
  batch.append ('string color '+c+'\n')
  batch.append ('string char size '+str(size)+'\n')
  batch.append ('string '+str(x+dx)+', '+str(y+dy)+'\n')
  batch.append ('string def "'+str(text)+'"\n')

def texts (xs,ys,ts,dx=0,dy=0,c='1',size=1):
  for i in xrange(len(xs)):
    text (xs[i],ys[i],ts[i],dx,dy,c,size)

def setp (title='',xlabel='',ylabel='',legx=0.25,legy=0.8,legsz=1.0,xlabsz=1.0,ylabsz=1.0,xbarlw=1.0,ybarlw=1.0,xticksz=1.0,yticksz=1.0):
  # title: Title
  # xlabel: x-axis label
  # ylabel: y-axis label
  # legx: Legend positoin in x-axis
  # legy: Legend positoin in y-axis
  # legsz: Legend size
  # xlabsz: x-axis label size
  # ylabsz: y-axis label size
  # xbarlw: x-bar line width
  # ybarlw: y-bar line width
  # xticksz: x-axis tick font size
  # yticksz: y-axis tick font size
  global batch
  batch.append ('title "'+title+'"\n')
  batch.append ('xaxis label "'+xlabel+'"\n')
  batch.append ('yaxis label "'+ylabel+'"\n')
  batch.append ('xaxis label char size '+str(xlabsz)+'\n')
  batch.append ('yaxis label char size '+str(ylabsz)+'\n')
  batch.append ('xaxis bar linewidth '+str(xbarlw)+'\n')
  batch.append ('yaxis bar linewidth '+str(ybarlw)+'\n')
  batch.append ('legend '+str(legx)+', '+str(legy)+'\n')
  batch.append ('legend char size '+str(legsz)+'\n')
  batch.append ('xaxis ticklabel char size '+str(xticksz)+'\n')
  batch.append ('yaxis ticklabel char size '+str(yticksz)+'\n')


def show (name='.temp',pfile=0):
  # name: File name. If not set, temporary plot will be deleted in the end.
  # pfile: if 1, save a ps file; if 0, do nothing
  global i, xmdat, batch

  if pfile == 0 or False: pass
  else:
    if pfile == 1 or True: pfile = name
    batch.append ('PRINT TO "'+pfile+'.ps"\n')
    batch.append ('DEVICE "EPS" OP "level2"\n')
    batch.append ('PRINT\n')

  bfile = '.temp.bfile'
  f = open (bfile,'w')
  for line in batch: f.write (line)

  # Define auto color here
  f.write ('map color 0 to (255, 255, 255), "white"\n')
  f.write ('map color 1 to (0, 0, 0), "black"\n')
  f.write ('map color 2 to (255, 0, 0), "red"\n')
  f.write ('map color 3 to (0, 0, 255), "blue"\n')
  f.write ('map color 4 to (0, 139, 0), "green4"\n')
  f.write ('map color 5 to (255, 128, 0), "orange"\n')
  f.write ('map color 6 to (255, 0, 255), "magenta"\n')
  f.write ('map color 7 to (166, 86, 40), "brown"\n')
  f.write ('map color 8 to (103, 7, 72), "maroon"\n')
  f.write ('map color 9 to (102, 0, 204), "purple"\n')
  f.write ('map color 10 to (0, 102, 51), "green"\n')
  f.write ('map color 11 to (64, 224, 208), "turquoise"\n')
  f.write ('map color 12 to (166, 206, 227), "lightblue"\n')
  f.write ('map color 13 to (178, 223, 138), "lightgreen"\n')
  f.write ('map color 14 to (251, 154, 153), "lightred"\n')
  f.write ('map color 15 to (253, 191, 111), "lightorange"\n')
  
  f.close()

  dfile = name+'.agr'
  f = open (dfile,'w')
  for line in xmdat: f.write (line)
  f.close()

  os.system ('xmgrace -type xydy -autoscale xy '+dfile+' -nosafe'+' -param '+bfile)
  # Remove temporary files
  os.system ('rm '+bfile)
  if dfile == '.temp.agr':
    os.system ('rm .temp.agr')
  i = 0
  xmdat = []
  batch = []
