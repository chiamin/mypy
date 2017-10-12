import sys
sys.path.append ('/home/chiamin/Projects/mypy')
sys.path.append ('/home/chiamin/Projects/mypy/QMC')
import Statistics as st
import pylab as pl
from QMC_analysis import *

def read_en (fname):
  f = open(fname)
  for line in f:
    if 'Measuring' in line: break

  Edat,wdat = [],[]
  for line in f:
    if 'E =' in line:
      Ei = float(line.split()[-1])
      Edat.append (Ei)
    if 'w =' in line:
      wi = float(line.split()[-1])
      wdat.append (wi)

  return Edat,wdat

def read_en_mult (fname,n,eqn=0):
  fnames = [fname+'_'+str(i)+'.out' for i in xrange(1,n+1)]
  Edat,wdat = [],[]
  for fname in fnames:
    Ei,wi = read_en (fname)
    Edat.extend (Ei[eqn:])
    wdat.extend (wi[eqn:])
  return Edat, wdat

def bin_dat (k, dat):
    'Binning the data by length k. Return: a shorter data'
    shortdata, i = [], 0
    while (i+k <= len(dat)):
      shortdata.append (st.mean (dat[i:i+k]))
      i += k
    # The last bin, which may contain less than k data
    if i != len(dat):
      shortdata.append (st.mean (dat[i:]))
    return shortdata

def block_dat (Edat,wdat, min_blknum=10, itvnum=40):
  Ewdat = [Ei*wi for Ei,wi in zip(Edat,wdat)]
  max_blksize = len(Edat)/min_blknum
  blksize_step = (max_blksize - 2) / itvnum
  if blksize_step <= 0: blksize_step = 1
  Es, errs = [],[]
  blksizes = range(2,max_blksize,blksize_step)
  for blocksize in blksizes:
    Ewdat_bin = bin_dat (blocksize, Ewdat)
    wdat_bin = bin_dat (blocksize, wdat)
    Eblk = [Ewi/wi for Ewi,wi in zip(Ewdat_bin,wdat_bin)]
    E,err = st.mean (Eblk,err=1)
    Es.append (E)
    errs.append (err)
  return Es,errs,blksizes

def mean_en (Edat,wdat,Npoint=200):
  blocksize = len(Edat)/Npoint
  if blocksize == 0: blocksize=1
  Ewdat = [Ei*wi for Ei,wi in zip(Edat,wdat)]
  Ewdat_bin = bin_dat (blocksize, Ewdat)
  wdat_bin = bin_dat (blocksize, wdat)
  Eblk = [Ewi/wi for Ewi,wi in zip(Ewdat_bin,wdat_bin)]
  xs = range(2,len(Eblk))
  Es = [st.mean(Eblk[:n]) for n in xs]
  errs = [st.err(Eblk[:n]) for n in xs]
  ts = [x*blocksize for x in xs]
  return ts,Es,errs

def main (fname,ncp,eqs,plot=0):
  if ncp == 0:
    Edat, wdat = read_en (fname)
  else:
    Edat, wdat = read_en_mult (fname,ncp,eqs)
  print 'number of data =', len(Edat)

  x = range(len(Edat))
  if plot:
    pl.plot (x,Edat,ls='None',marker='.')
    pl.xlabel ('$\\tau$',fontsize=20)
    pl.ylabel ('$E$',fontsize=20)
    pl.show()

  if plot:
    pl.hist (Edat[eqs:],bins=100)
    pl.title ('Histogram of E')
    pl.show()

  Edat = Edat[eqs:]
  wdat = wdat[eqs:]
  print 'equilibrium steps =',eqs

  #uncorr_data, ks, err, corrtime = binning_prof (Edat, knum=200, NBmin=100, plot=True)

  Es,errs,blksizes = block_dat (Edat, wdat)
  if plot:
    pl.plot (blksizes,errs,ls='None',marker='.')
    pl.xlabel ('bin size',fontsize=20)
    pl.ylabel ('error bar',fontsize=20)
    pl.show()

  ts,Ems,errms = mean_en (Edat,wdat)
  if plot:
    pl.errorbar (ts,Ems,errms)
    pl.xlabel ('$\\tau$',fontsize=20)
    pl.ylabel ('$E$',fontsize=20)
    pl.show()

  #equi_prof (Edat, plot=True, plotn=1000)

  print 'E from blocks =',Es[-1]
  print 'err =',max(errs)
  print 'block size =',blksizes[-1]
  print Es[-1],errs[-1]
  return Es[-1],errs[-1]

if __name__ == '__main__':
  fname = sys.argv[1]
  ncp = int(sys.argv[2])
  eqs = 0
  if len(sys.argv) > 3: eqs = int(sys.argv[3])
  main(fname,ncp,eqs,plot=1)
