import sys, os

# The first argument <fname> is the output of measure.exe
# The second argument <parafile> is the input file of DMRG calculation
# The third and fourth arguments are truncation error and m
# Output files <fname>.temp and <fname>.temp.ps

fname = sys.argv[1]
if len(sys.argv) > 2:
  parafile = sys.argv[2]
if len(sys.argv) > 4:
  trunc = float(sys.argv[3])
  m = int(sys.argv[4])


def main():
  comb_file (fname)
  if len(sys.argv) > 2:
    addlocalh (fname+'.temp',parafile)
  os.system ('plothsz.pl '+fname+'.temp')
  if len(sys.argv) > 4:
    addlabels (fname+'.temp.ps',trunc,m)
  print '\n',fname+'.temp','\n'
  os.system ('rm '+fname+'.temp')

def comb_file (fil):
  newfile = []
  f = open (fil)
  for line in f:
    if line[:2] == '**': pass
    elif 'Making input group' in line: pass
    elif 'Got ' in line: pass
    else:
      newfile.append (line)
  f.close()

  try: f = open (fil+'.temp','w')
  except: print 'Cannot open file', fil+'.temp'
  for line in newfile:
    f.write (line)
  f.close()


def addlocalh (fname, parafile):
  localh = []
  mode = ''
  f = open (parafile)
  for line in f:
    if 'localmuh' in line:
      mode = 'localmuh'
      continue
    if mode == 'localmuh' and all(x in line for x in ['x','y','mu','h']):
      mode = 'read'
      continue
    if mode == 'read' and '}' in line: break
    if 'Making input group' in line: break
    if mode == 'read':
      x,y,mu,h = line.split()
      localh.append (x+'\t'+y+'\t'+h+'\tmagfield\n')
  f.close()

  try: f = open (fname,"a")
  except: print 'Cannot open file', fil+'.temp'
  for line in localh:
    f.write (line)
  f.close()


def addlabels (fname, trunc, m):

  def get_bounding (f):
    for line in f:
      if 'BoundingBox' in line:
        xmin,ymin,xmax,ymax = map (int, line.split()[1:])
        return xmin,ymin,xmax,ymax

  def add_label (string, labels, xmin,ymin,xmax):
    l = len (string) * 10
    if xmax-xmin < l:
      dl = l - (xmax - xmin)
      xmin -= dl
      xmax += dl
    xplace = (xmax - xmin)/2 - l/2+25
    ymin -= 30
    st = str(xplace)+' '+str(ymin)+' moveto ('+string+') show\n'
    labels.append (st)
    ymin -= 30
    return st, xmin, ymin, xmax

  def write (f,xmin,ymin,xmax,ymax,labels):
    for i in xrange(len(f)):
      line = f[i]
      if 'BoundingBox' in line:
        f[i] = "%%BoundingBox: "+str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)+'\ngsave\n'
      elif 'showpage' in line:
        del f[i]
    f.append ('grestore\n')
    f.append ('% **********************************\n')
    f.append ('/Times-Roman findfont 24 scalefont setfont\n')
    for label in labels:
      f.append (label)
    f.append ('% **********************************\n')
    f.append ('showpage\n')

    fout = open (fname,'w')
    for line in f:
      fout.write (line)
    fout.close()

  fin = open (fname)
  f = fin.readlines()
  fin.close()

  xmin,ymin,xmax,ymax = 0,0,0,0
  labels = []

  xmin,ymin,xmax,ymax = get_bounding (f)

  # Truncation error and m
  trunc = "%.3g" % trunc
  string = "m = "+str(m)+", truncated = "+trunc
  labels, xmin, ymin, xmax = add_label (string, labels, xmin,ymin,xmax)

  write (f,xmin,ymin,xmax,ymax,labels)

main()
