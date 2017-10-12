import sys
sys.path.append('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut

def get_N_mu (fname):
    f = open (fname)
    for line in f:
        if 'mu =' in line:
            N = len(line.split())-2
            return N
    raise KeyError

def get_mus (fname):
    f = open (fname)
    for line in f:
        if 'mu =' in line:
            mus = map(float,line.split()[2:])
            return mus
    raise KeyError

def get_meas_multi_states (f,lx,ly,N_states,sweep=0):
  if sweep != 0:
    f,swp = ut.get_sweep (f)

  N = lx*ly
  xs,ys,nups,ndns,ns,szs,hs = [],[],[],[],[],[],[]
  for i in xrange(N_states):
    xs.append ([])
    ys.append ([])
    nups.append ([])
    ndns.append ([])
    ns.append ([])
    szs.append ([])
    hs.append ([])

  for i in xrange(N,0,-1):
    x,y = ut.getxy (i,lx,ly)

    line = ''
    for line in f:
        if 'Sweep=' in line:
            swp = int(line.split(',')[0].split('=')[-1])
        if 'Max_m=' in line:
            m = int(line.split('=')[-1])
        if 'Measure on site '+str(i) in line:
            j = int(line.split()[-1])

            f,nup,ndn,n,sz = ut.get_mea(f)

            xs[j].append(x)
            ys[j].append(y)
            nups[j].append(nup)
            ndns[j].append(ndn)
            ns[j].append(n)
            szs[j].append(sz)
            hs[j].append(1-n)

            if j == N_states-1: break

    if line == '':
        raise KeyError

  return f,swp,m,xs,ys,nups,ndns,ns,szs,hs

