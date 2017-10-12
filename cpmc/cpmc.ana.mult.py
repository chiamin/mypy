import sys
sys.path.append ('/home/chiamin/Projects/mypy')
sys.path.append ('/home/chiamin/Projects/mypy/QMC')
import QMC_analysis as mc
import pylab as pl
import numpy as np
from CMC_file import *
from math import exp

ff = sys.argv[1]
Ncp = sys.argv[2]
neq = 6
#binsize = [1,10,1]
prof = 1
prof_i = 1
write_samples = 0

for arg in sys.argv[3:]:
  if 'neq' in arg:
    neq = int(arg.split('=')[-1])
  if arg == 'noplot':
    prof = 0

#if len(sys.argv) > 3:
#  prof = int(sys.argv[3])
#if len(sys.argv) > 4:
#  write_samples = int(sys.argv[4])

def main ():
  Lx,Ly = getLxy (ff+'.cp1.out')

  Es, nups, ndns, nupmixs, ndnmixs = [],[],[],[],[]
  for i in xrange(1,int(Ncp)+1):
    if i == 1:
      para = ff+'.cp'+str(i)+'.out'
      f = open(para)
      for line in f:
        if 'Making input group basic' in line: break
        print line.rstrip('\n')

    fname = ff+'.cp'+str(i)+'.out'
    #print fname
    Ei,nupmixi, ndnmixi, nupi,ndni = read_cpmc (fname, ['E','up_density (mix estimator)','dn_density (mix estimator)','up_density (backward propagation)','dn_density (backward propagation)'])
    Es += Ei[neq:]
    nups += nupi[neq:]
    ndns += ndni[neq:]
    nupmixs += nupmixi[neq:]
    ndnmixs += ndnmixi[neq:]

    if prof and i == prof_i:
      #obs = Ei[neq:]
      nnup = zip(*nupi)[prof_i]
      nndn = zip(*ndni)[prof_i]
      nnupmix = zip(*nupmixi)[prof_i]
      nndnmix = zip(*ndnmixi)[prof_i]
      hh = [1-nup-ndn for nup,ndn in zip(nnup,nndn)]
      hhmix = [1-nup-ndn for nup,ndn in zip(nnupmix,nndnmix)]

      obs = hh[neq:]
      pl.plot (range(len(obs)), obs)
      mc.equi_prof (obs, plot=True, plotn=1000)
      obsmix = hhmix[neq:]
      pl.plot (range(len(obsmix)),obsmix)
      mc.equi_prof (obsmix, plot=True, plotn=1000)

  if Ncp == '0':
    para = ff+'.in'
    with open(para, 'r') as fin:
      print fin.read()
    fname = ff+'.out'
    Ei,nupmixi, ndnmixi,nupi,ndni = read_cpmc (fname, ['E','up_density (mix estimator)','dn_density (mix estimator)','up_density (backward propagation)','dn_density (backward propagation)'])
    Es += Ei[neq:]
    nups += nupi[neq:]
    ndns += ndni[neq:]
    nupmixs += nupmixi[neq:]
    ndnmixs += ndnmixi[neq:]

  Nmea = len(Es)
  BinMin = max(1,Nmea/10)
  BinMax = min(BinMin+20,Nmea/4)
  binsize = [BinMin,BinMax,1]

  print 'Equilibrium skipped:',neq
  print 'Bin size [min,max,itv]:',binsize
  print 'Number of measurements =', len(Es)

  hs, szs, hmixs, szmixs = [],[],[],[]
  for site in range(1,Lx*Ly+1):
    j = site-1
    nnup = zip(*nups)[j]
    nndn = zip(*ndns)[j]
    nnupmix = zip(*nupmixs)[j]
    nndnmix = zip(*ndnmixs)[j]
    hs.append( [1-nup-ndn for nup,ndn in zip(nnup,nndn)])
    szs.append( [0.5*(nup-ndn) for nup,ndn in zip(nnup,nndn)])
    hmixs.append( [1-nup-ndn for nup,ndn in zip(nnupmix,nndnmix)])
    szmixs.append( [0.5*(nup-ndn) for nup,ndn in zip(nnupmix,nndnmix)])


  if prof:
    #ptemp = Es
    ptemp = hmixs[prof_i-1]
    pl.plot (range(len(ptemp)), ptemp)
    mc.equi_prof (ptemp, plot=True, plotn=1000)
    mc.binning_prof (ptemp, knum=200, NBmin=20, plot=True)
    #exit()

  if 0:#write_samples:
    writefile (ff+'.en.samples',[range(len(Es)),Es])
    for site in range(1,Lx*Ly+1):
      hi, szi = hs[site-1], szs[site-1]
      writefile (ff+'.h'+str(site)+'.samples',[range(len(hi)),hi])
      writefile (ff+'.sz'+str(site)+'.samples',[range(len(szi)),szi])


  #printavg (Es,nups,ndns)
  E,Eerr = binning_one (Es,binsize)
  h,herr = binning_many (hs,binsize)
  sz,szerr = binning_many (szs,binsize)
  hmix,hmixerr = binning_many (hmixs,binsize)
  szmix,szmixerr = binning_many (szmixs,binsize)
  print 'E =',E,'+-',Eerr
  print 'x y sz szerr h herr hmix hmixerr szmix szmixerr'
  for i in xrange(len(h)):
      x = i / Ly + 1
      y = i % Ly + 1
      print x,y,sz[i],szerr[i],h[i],herr[i],szmix[i],szmixerr[i],hmix[i],hmixerr[i]

def binning_one (Es,binsize):
  E,Eerr = mc.binning2 (Es, binsize[0], binsize[1], binsize[2])
  return E,Eerr

def binning_many (hs,binsize):
  h,herr = [],[]
  for hi in hs:
    h_tmp, e_tmp = mc.binning2 (hi, binsize[0], binsize[1], binsize[2])
    h.append (h_tmp)
    herr.append (e_tmp)
  return h,herr

def printavg (Es,nups,ndns):
  #Es, nups, ndns = read_cpmc (ff, ['E','up_density','dn_density'])

  E,Eerr = mc.binning2 (Es, binsize[0], binsize[1], binsize[2])

  nup, nuperr, ndn, ndnerr = [],[],[],[]
  for ni in zip(*nups):
    n,e = mc.binning2 (ni, binsize[0], binsize[1], binsize[2])
    nup.append (n)
    nuperr.append (e)
  for ni in zip(*ndns):
    n,e = mc.binning2 (ni, binsize[0], binsize[1], binsize[2])
    ndn.append (n)
    ndnerr.append (e)
  nup = np.array(nup).reshape(Lx,Ly)
  ndn = np.array(ndn).reshape(Lx,Ly)
  nuperr = np.array(nuperr).reshape (Lx,Ly)
  ndnerr = np.array(ndnerr).reshape (Lx,Ly)

  n  = nup + ndn
  sz = nup - ndn
  nerr = nuperr + ndnerr
  h = 1. - n

  print 'E = ', E, Eerr
  print 'n up =\n', nup
  print 'n down =\n', ndn
  print 'n error =\n', nerr
  print 'Total density =\n', n
  print 'Hole density =\n', h
  print 'Sz =\n', sz


def read_cpmc (ff,obs):
  dats = []
  for i in range(len(obs)): dats.append([])
  f = open (ff,'r')
  for line in f:
    for i in range(len(obs)):
      ostr = ' '+obs[i] + ' = '
      if ostr in line:
        pos = line.find (ostr) + len(ostr)
        dstr = line[pos:].rstrip('\n ')
        dat = [float(di) for di in dstr.split(' ')]
        if len(dat) == 1: dats[i].append (dat[0])
        else: dats[i].append (dat)
  if len(obs) == 1: return dats[0]
  else: return dats

def getLxy (fname):
  f = open (fname)
  for line in f:
    if 'Lx =' in line:
      lx = int(line.split()[-1])
    elif 'Ly =' in line:
      ly = int(line.split()[-1])
      return lx,ly

main()
