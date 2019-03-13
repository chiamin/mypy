import sys
sys.path.append ('/home/chiamin/Projects/mypy')
import fitfun as ff
import grace
import pylab as pl

def get_val (fname,key,typ=float):
  f = open (fname)
  for line in f:
    if key in line:
      return typ(line.split()[-1])
  print key,'not found'
  raise Exception

def get_first_m (fname):
  f = open (fname)
  for line in f:
    if all(i in line for i in ['m','cutoff','niter','noise']):
      break
  for line in f:
    return int(line.split()[0])
  print 'not found'
  raise Exception

def getlxy (fname):
  f = open (fname)
  for line in f:
    if 'Got' in line and '.Lx' in line:
      lx = int(line.split(' = ')[-1])
    if 'Got' in line and '.Ly' in line:
      ly = int(line.split(' = ')[-1])
      return lx,ly
  print "Couldn't found lx,ly"
  raise Exception

def trunerr (fname):
  lx,ly = getlxy (fname)
  Nsites = lx*ly

  f = open (fname)
  sweep = -1
  sweeps, cutoffs, ms, terr, E, Eps = [],[],[],[],[],[]
  for line in f:
    if 'Sweep=' in line:
      tmp = line.split(',')
      sweep = int(tmp[0].split('=')[-1])
      HS    = int(tmp[1].split('=')[-1])
      Bond  = line.split('=')[-1].strip()
      if HS==1 and (Bond=='(1,2)' or Bond.split('/')[0]=='1'):
        sweeps.append (sweep)
        cutoffs.append (-1)
        ms.append (-1)
        terr.append ([])
        E.append (-1.e12)
        Eps.append (-1.e12)
        for linetmp in f:
          if 'Truncated to Cutoff=' in linetmp:
            tmp = linetmp.split(',')
            cutoff = float(tmp[0].split('=')[-1])
            m = int(tmp[1].split('=')[-1])
            cutoffs[-1] = cutoff
            ms[-1] = m
            break

    if 'Trunc. err=' in line:
      erri = float(line.split(',')[0].split('=')[-1])
      terr[-1].append (erri)

    if ' Energy after sweep' in line:
      en = float(line.split()[-1])
      E[-1] = en
      Eps[-1] = en/Nsites

  if E[-1] == -1.e12:
    del sweeps[-1]
    del cutoffs[-1]
    del ms[-1]
    del terr[-1]
    del E[-1]
    del Eps[-1]

  for i in xrange(len(terr)):
    terr[i] = sum(terr[i])/len(terr[i])

  #return re
  return sweeps, cutoffs, ms, terr, E, Eps

def trunerr2 (fname,mmin=0,mmax=100000000,itv=-1,verbose=True):
  sweeps, cutoffs, ms, terr, E, Eps = trunerr (fname)

  if verbose:
      for i in zip(*[sweeps, cutoffs, ms, terr, E, Eps]): print i

  re_swps, re_cutoff, re_ms, re_terr, re_E, re_Eps = [],[],[],[],[],[]
  for i in xrange(len(ms)-1):
    #if ms[i+1] != ms[i] or (i == len(ms)-2 and ms[-1] not in re_ms):
        #if i == len(ms)-2: i += 1
        re_swps.append (sweeps[i])
        re_cutoff.append (cutoffs[i])
        re_ms.append (ms[i])
        re_terr.append (terr[i])
        re_E.append (E[i])
        re_Eps.append (Eps[i])

  return re_swps, re_cutoff, re_ms, re_terr, re_E, re_Eps

def get_eachm (ms, mmin=0, *obss):
  re_ms = []
  re = [[] for i in xrange(len(obss))]
  for i in xrange(len(ms)-1):
    if ms[i] > mmin and (ms[i+1] != ms[i] or (i == len(ms)-2 and ms[-1] not in re_ms)):
        #if i == len(ms)-2: i += 1
        re_ms.append (ms[i])
        for j in xrange(len(obss)):
            re[j].append (obss[j][i])
  return [re_ms] + re

  '''
  if ms[-1] not in re_ms:

  firstm = get_first_m (fname)
  if mmin < firstm:
    mmin = firstm
  if itv == -1:
    itv = get_val (fname,'nsweep',int)
  gotn = False
  nend = None
  for i in xrange(len(ms)):
    if ms[i] >= float(mmin) and not gotn:# and ms[i-1] == ms[i]:
      n = i+itv-1
      gotn = True
    if ms[i] >= float(mmax):
      nend = i+itv
      break
  sweeps, cutoffs, ms, terr, E, Eps = sweeps[n:nend:itv], cutoffs[n:nend:itv], ms[n:nend:itv], terr[n:nend:itv], E[n:nend:itv], Eps[n:nend:itv]
  return sweeps, cutoffs, ms, terr, E, Eps'''

def get_en (fname,mmin=500,mmax=10000000,plot=False,order=1,itv=-1,verbose=True,fitpts=0,fac=1.):
  sweep, cutoff, ms, terr, E, Eps = trunerr2 (fname, mmin, mmax, itv=itv ,verbose=verbose)
  ms, sweep, cutoff, terr, E, Eps = get_eachm (ms, mmin, sweep, cutoff, terr, E, Eps)
  terrs, Epss = [],[]
  if verbose:
      print 'sweep\tcutoff\tm \ttrunerr\t\t\tE\t\tEpersite'
  for i in xrange(len(sweep)):
    if verbose:
      print str(sweep[i]).ljust(5),str(cutoff[i]).ljust(7),str(ms[i]).ljust(4),str(terr[i]).ljust(20),str(E[i]).ljust(20),Eps[i]
    if ms[i] >= mmin and ms[i] <= mmax:
      terrs.append (terr[i])
      Epss.append (Eps[i])

  Epss = [i*fac for i in Epss]
  terrs = [i*fac for i in terrs]

  terrs = terrs[-fitpts:]
  Epss = Epss[-fitpts:]

  fit  = ff.polyfit (terrs,Epss,order=order,err=terrs)
  fitx = terrs+[0.]
  fity = ff.polyf (fit,fitx)
  if verbose:
    print fit
  Efit = fity[-1]
  Eerr = 0.2*abs(Efit-Epss[-1])
  print 'E =',Efit,'+-',Eerr

  if plot:
    #pl = grace.new()
    pl.plot (terrs,Epss,'o-k')
    pl.plot (fitx,fity,'-r')
    pl.xlabel ('truncation error',fontsize=18)
    pl.ylabel ('energy per site',fontsize=18)
    pl.show()
    #pl.setp (xlabel='Truncated weight',ylabel='Energy')
    #grace.show()
    #grace.clean()

  return Efit,Eerr

def full_sweeps_en (fname):
  sweeps, cutoffs, ms, terr, E, Eps = trunerr (fname)
  fig, ax1 = pl.subplots()
  ax1.plot (range(len(ms)),ms)
  ax2 = ax1.twinx()
  ax2.plot (range(len(ms)),Eps,'o-')
  pl.show()


if __name__ == '__main__':
  if '-check' in sys.argv:
      full_sweeps_en (sys.argv[1])
      exit()

  mmin=-1
  mmax=10000000
  if len(sys.argv) > 2:
    mmin=int(sys.argv[2])
    if len(sys.argv) > 3:
        mmax=int(sys.argv[3])
  get_en (sys.argv[1], mmin=mmin, mmax=mmax, itv=2, plot=1)
