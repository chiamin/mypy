import sys, os
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import trunerr as te
import numpy as np
import utility as ut

def file_get (f, key, typ=str):
  for line in f:
    if key in line:
      return f, typ(line.split()[-1])
  print key,'not found'
  raise KeyError

def file_goto (f, key):
  for line in f:
    if key in line:
      return f
  print key,'not found'
  raise KeyError

def get_mea (f):
  for line in f:
    if 'n_up' in line: nup = float(line.split()[-1])
    if 'n_dn' in line: ndn = float(line.split()[-1])
    if 'N_tot' in line: n = float(line.split()[-1])
    if 'sz' in line: sz = float(line.split()[-1])
    if 'Sweep=' in line: break
  return f, nup, ndn, n, sz

def getxy (i, lx, ly):
# i starts from 1
# x,y start from 1
  i,lx,ly = int(i-1),int(lx),int(ly)
  return i/ly+1, i%ly+1

'''def get_meas (f,lx,ly,sweep=0):
  if sweep != 0:
    f = file_goto (f,'Sweep='+str(sweep))

  N = lx*ly
  xs,ys,nups,ndns,ns,szs,hs = [],[],[],[],[],[],[]
  for i in xrange(N,0,-1):
    x,y = getxy (i,lx,ly)

    f = file_goto (f,'Measure on site '+str(i))
    f,nup,ndn,n,sz = get_mea(f)

    xs.append(x)
    ys.append(y)
    nups.append(nup)
    ndns.append(ndn)
    ns.append(n)
    szs.append(sz)
    hs.append(1-n)

  return f,xs,ys,nups,ndns,ns,szs,hs
'''
def get_lastm_pos (fname,N,start=''):
  # Jump to the start line
  f = open (fname)
  for line in iter(f.readline, ''):
    if start in line:
      break

  # Store the positions of starting the measures
  ms, pos = [],[]
  for line in iter(f.readline, ''):
    if 'HS=1, Bond=('+str(N-1)+','+str(N)+')' in line:
      # read m and get position
      for line in iter(f.readline, ''):
        if 'Max_m' in line:
          m = int(line.split('=')[-1])
          break
      p = f.tell()
      # read next m
      mnext = 0
      for line in iter(f.readline, ''):
        if 'HS=1, Bond=(1,2)' in line: break
      for line in iter(f.readline, ''):
        if 'Max_m' in line:
          mnext = int(line.split('=')[-1])
          break
      # store the position if m != mnext
      if mnext != 0 and m != mnext:
        ms.append (m)
        pos.append (p)
  #if mnext != 0 and m not in ms:
  if m not in ms:
    ms.append (m)
    pos.append (p)

  f.close()
  return ms, pos

def mea_obs (f,lx,ly,subkey=''):
    N = lx*ly
    terri, tn = 0., 0.
    xs,ys,nups,ndns,ns,szs,hs = [],[],[],[],[],[],[]
    for i in xrange(N,0,-1):
      for line in f:
        if 'Max_m' in line:
          m = int(line.split('=')[-1])
        if 'Trunc. err=' in line:
          erri = float(line.split(',')[0].split('=')[-1])
          terri += erri
          tn += 1.
          break

      x,y = getxy (i,lx,ly)
      try:
          f = file_goto (f,'Measure on site '+str(i)+subkey)
      except KeyError:
          print 'Cannot find:','Measure on site '+str(i)
          raise KeyError
      f,nup,ndn,n,sz = get_mea(f)

      xs.append(x)
      ys.append(y)
      nups.append(nup)
      ndns.append(ndn)
      ns.append(n)
      szs.append(sz)
      hs.append(1-n)
    return m, terri/tn, xs,ys,nups,ndns,ns,szs,hs

def get_meas_ms_once (fname,start='',mode='eachm',subkey=''):
# mode can be 'eachm' or 'all'
  f = open (fname)
  f,lx = file_get (f,'Lx',int)
  f,ly = file_get (f,'Ly',int)
  N = lx * ly

  # Read the observables
  obss, terrs = [],[]
  if mode == 'eachm':
    ms, pos = get_lastm_pos (fname,N,start)
    for p in pos:
        f.seek (p)
        try:
            m, terr, xs,ys,nups,ndns,ns,szs,hs = mea_obs (f,lx,ly,subkey)
        except KeyError:
            ms = ms[:len(obss)]
            break
        print 'm=',m
        terrs.append (terr)
        obss.append ([xs,ys,nups,ndns,ns,szs,hs])
  elif mode == 'all':
    ms = []
    while True:
        try:
            file_goto (f,start)
            m, terr, xs,ys,nups,ndns,ns,szs,hs = mea_obs (f,lx,ly,subkey)
        except KeyError:
            break

        ms.append (m)
        terrs.append (terr)
        obss.append ([xs,ys,nups,ndns,ns,szs,hs])
  return ms, terrs, obss

def getmax (vals, crit):
  maxx = max(vals);
  if maxx > crit:
    for val in np.arange(0.0, 2.00001, 0.05):
      if maxx <= val+0.015 and maxx > val-0.035:
        maxx = val
        break
  else:
    maxx = round (maxx * 10000) / 10000
    if maxx < 0.0001: maxx = 0.0001;
  return maxx;

def os_exe (command):
  print command
  os.system(command)

def addlocalh (fname, parafile):
  localh = []
  mode = ''
  f = open (parafile)
  for line in f:
    if 'localmuh\n' in line:
      print line
      mode = 'localmuh'
      continue
    if mode == 'localmuh' and all(x in line for x in ['x','y','mu','h']):
      mode = 'read'
      continue
    if mode == 'read' and '}' in line: break
    if 'Making input group' in line: break
    if mode == 'read':
      x,y,mu,h = line.split()
      if float(h) != 0.:
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
        xmin,ymin,xmax,ymax = map (float, line.split()[1:])
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

def hsz_plot_dat (fname,xs,ys,szs,hs,suf='',latt='ordinary',replace=False):
  f = open (fname)
  f,lx = file_get (f,'Lx',int)
  f,ly = file_get (f,'Ly',int)

  maxsz = getmax (szs, crit=0.03)
  maxh  = getmax (hs, crit=0.02)

  hszstr = '1\t1\t'+str(lx)+'\t'+str(ly)+'\t'+str(maxsz)+'\t'+str(maxh)+'\n'
  for i in xrange(len(hs)):
    hszstr += '  '+str(xs[i])+'  '+str(ys[i])+'  '+str(szs[i])+'  '+str(hs[i])+'\n'

  hszfile = fname+suf+'.hsz'
  if not replace:
    n = 2
    while os.path.isfile (hszfile+'.ps'):
      hszfile = hszfile.replace('.hsz','_'+str(n)+'.hsz')
      n += 1
  fw = open(hszfile,'w')
  fw.write (hszstr)
  fw.close()

  addlocalh (hszfile, fname)

  if latt == 'ordinary': perl = 'plothsz.pl'
  elif latt == 'rot45':  perl = 'plothsz.diag.pl'

  os_exe (perl+' '+hszfile)
  os_exe ('rm '+hszfile)
  os_exe ('rm tmp')
  return hszfile+'.ps'

if __name__ == '__main__':
  fname = sys.argv[1]
  mmin = 0
  if len(sys.argv) > 2: mmin = sys.argv[2]

  latt = 'ordinary'
  for arg in sys.argv:
    if arg == '-rot': latt = 'rot45'

  sweeps, cutoffs, ms, terr, E, Eps = te.trunerr2 (fname,mmin)

  f = open (fname)
  f,lx = file_get (f,'Lx',int)
  f,ly = file_get (f,'Ly',int)
  print sweeps
  f,swp,m,xs,ys,nups,ndns,ns,szs,hs = ut.get_meas (f,lx,ly,sweeps[-1])
  psfile = hsz_plot_dat (fname,xs,ys,szs,hs,latt=latt,replace=True)

  addlabels (psfile, terr[-1], ms[-1])
