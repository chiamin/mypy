import sys
sys.path.append ('/home/chiamin/Projects/mypy')
from CMC_file import *
sys.path.append ('/home/chiamin/Projects/mypy/dmrg')
import utility as ut
import numpy as np
import fitfun as ff
import grace
import pylab as pl

def ext_en (f1, f2, mmin=500, mmax=10000000, rm_mu=False, plot=False):
  m, trun, E = ext_ens (f1,f2,mmin,mmax,rm_mu)
  print 'm =',m
  if plot:
    pl.plot (trun,E,marker='o')

  fitx,fity,stdev = ff.myfit (trun,E,werr=trun)
  if plot:
    pl.plot (fitx,fity,c='r')
    pl.show()

  return fity[-1], 0.2*abs(fity[-1]-E[-1])

def ext_ens (f1, f2, mmin=500, mmax=10000000, rm_mu=False):
  lx1,ly1 = ut.getLxy (f1)
  lx2,ly2 = ut.getLxy (f2)
  N1,N2 = lx1*ly1, lx2*ly2

  E1,trun1,m1,sw1 = map(np.array, get_discwt (f1,mmin,mmax,rm_mu))
  E2,trun2,m2,sw2 = map(np.array, get_discwt (f2,mmin,mmax,rm_mu))
  iend = 0
  for i in xrange(len(m1)):
    if i >= len(m2): break
    if m1[i] == m2[i]: iend = i+1
    else: break
  E1,trun1,m1,sw1 = E1[:iend],trun1[:iend],m1[:iend],sw1[:iend]
  E2,trun2,m2,sw2 = E2[:iend],trun2[:iend],m2[:iend],sw2[:iend]

  E = (E2-E1) / float(N2-N1)
  trun = 0.5*(trun1 + trun2)
  return m1, trun, E

def get_discwt (fname,mmin=500,mmax=10000000,rm_mu=False):
  lx,ly = ut.getLxy (fname)
  N = lx*ly

  dat = readprint ('discwt2.p '+fname)
  if float(dat[-1][0]) == 0.: del(dat[-1])
  E,trun,m,sw = [],[],[],[]
  mpre = 0
  for di in dat:
    Ei,tri,mi,swi = float(di[1]),float(di[2]),int(di[3]),int(di[4])
    if mi >= mmin and mi <= mmax and mi == mpre and Ei < 1e20: 
      if rm_mu:
        mu = ut.getmu (fname)
        Ei += mu * ut.getN (fname,swi)
      E.append (Ei)
      trun.append (float(di[2]))
      m.append (int(di[3]))
      sw.append (swi)

    mpre = int(di[3])
  return E,trun,m,sw

def plot_en (lx,ly,E,trun,plot=True,order=1,plt='matplot',show=True,lb=''):
  E = [Ei/(lx*ly) for Ei in E]

  fit = ff.polyfit (trun,E,order=order,err=trun)
  fitx = trun+[0.]
  fity = ff.polyf (fit,fitx)
  Efit = fity[-1]
  Eerr = 0.2*abs(Efit-E[-1])
  #print 'E =',Efit,'+-',Eerr

  if plot:
    if plt == 'matplot':
      pl.plot (trun,E,marker='o',c='k',label=lb)
      pl.plot (fitx,fity,c='r')
      pl.xlabel ('Truncated weight')
      pl.ylabel ('Energy')
      if show: pl.show()
    else: # plt is a grace object
      plt.plot (trun,E,ls=0,legend=lb)
      plt.plot (fitx,fity,symb=0,c='same')
      plt.setp (xlabel='Truncated weight',ylabel='Energy',legx=0.2)
      if show:
        grace.show()
        grace.clean()

  return Efit,Eerr

def get_en (fname,mmin=500,mmax=10000000,plot=False,order=1):
  E,trun,m,sw = get_discwt (fname,mmin=mmin,mmax=mmax)
  print m
  lx,ly = ut.getLxy (fname)
  E = [Ei/(lx*ly) for Ei in E]

  fit = ff.polyfit (trun,E,order=order,err=trun)
  fitx = trun+[0.]
  fity = ff.polyf (fit,fitx)
  Efit = fity[-1]
  Eerr = 0.2*abs(Efit-E[-1])
  #print 'E =',Efit,'+-',Eerr

  if plot:
    pl = grace.new()
    pl.plot (trun,E)
    pl.plot (fitx,fity,symb=0)
    pl.setp (xlabel='Truncated weight',ylabel='Energy')
    grace.show()
    grace.clean()

  return Efit,Eerr

