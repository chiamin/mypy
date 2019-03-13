import sys

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
    if 'n_up =' in line: nup = float(line.split()[-1])
    if 'n_dn =' in line: ndn = float(line.split()[-1])
    if 'N_tot =' in line: n = float(line.split()[-1])
    if 'sz =' in line:
        sz = float(line.split()[-1])
        return f, nup, ndn, n, sz
  raise KeyError

def get_mea_obs (f,obs,fromkey=''):
  vals = [float('Nan') for i in xrange(len(obs))]
  for line in f:    
    for i in xrange(len(obs)):
        if obs[i] in line:
            vals[i] = float(line.split()[-1])
    if 'Sweep=' in line: break
  return f, vals

def get_meas_obs (f,N,obs,sweep=0,start=''):
  #with open(fname) as f:
      if sweep != 0:
        f = file_goto (f, 'Sweep='+str(sweep))
      if start != '':
        f = file_goto (f, start)

      obss = [[] for i in xrange(len(obs))]
      sites = xrange(N,0,-1)
      for i in sites:
        for line in f:
            if 'Sweep=' in line:
                swp = int(line.split(',')[0].split('=')[-1])
            if 'Max_m=' in line:
                m = int(line.split('=')[-1])
            if 'Measure on site '+str(i) in line:
                break
        f,vals = get_mea_obs (f,obs)

        for j in xrange(len(obs)):
            obss[j].append (vals[j])

      return f,swp,m,sites,obss

def get_sweep (f,sweep):
  for line in f:
    if 'Sweep='+str(sweep) in line:
        swp = int(line.split(',')[0].split('=')[-1])
        return f, swp
  raise KeyError

def getLxy (fname):
  f = open (fname)
  f,lx = file_get (f,'Lx',int)
  f,ly = file_get (f,'Ly',int)
  f.close()
  return lx,ly

def getxy (i, lx, ly):
# i starts from 1
# x,y start from 1
  i,lx,ly = int(i-1),int(lx),int(ly)
  return i/ly+1, i%ly+1

def get_meas (f,lx,ly,sweep=0):
  if sweep != 0:
    f = file_goto (f, 'Start main sweeps')
    f,swp = get_sweep (f,sweep)

  N = lx*ly
  xs,ys,nups,ndns,ns,szs,hs = [],[],[],[],[],[],[]
  for i in xrange(N,0,-1):
    x,y = getxy (i,lx,ly)

    for line in f:
        if 'Sweep=' in line:
            swp = int(line.split(',')[0].split('=')[-1])
        if 'Max_m=' in line:
            m = int(line.split('=')[-1])
        if 'Measure on site '+str(i) in line:
            break
    f,nup,ndn,n,sz = get_mea(f)

    xs.append(x)
    ys.append(y)
    nups.append(nup)
    ndns.append(ndn)
    ns.append(n)
    szs.append(sz)
    hs.append(1-n)

  return f,swp,m,xs,ys,nups,ndns,ns,szs,hs

def get_pairing (f,sweep=0,key='Pairing'):
    if sweep != 0:
        f = file_goto (f, 'Start main sweeps')
        f,swp = get_sweep (f,sweep)

    delta = dict()
    for line in f:
        if 'Sweep=' in line:
            swp = int(line.split(',')[0].split('=')[-1])
        if 'Max_m=' in line:
            m = int(line.split('=')[-1])
        if key in line:
            break
    for line in f:
        tmp = line.split()
        try:
            x1,y1,x2,y2 = map(int,tmp[:4])
            di = float(tmp[-1])
            delta[x1,y1,x2,y2] = di
        except ValueError:
            return f,swp,m,delta

    raise EOFError
