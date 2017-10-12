import sys
sys.path.append ('/home/bluewhite/Projects/mypy')
sys.path.append ('/home/bluewhite/Projects/mypy/dmrg')
from CMC_file import *
import pylab as pl
import numpy as np
import get_discwt as discwt
import fitfun as ff
import random as rand
from math import sqrt

def en_extra_x (files,mlowerlim=0,mupperlim=1000000000,fitorder=2,plot=True,floc='.',dloc='.'):
  # get non-error energies
  if type(mlowerlim)==list:
    temp = []
    for i in range(len(files)):
      temp.append (en_extra_err (files[i],mlowerlim[i],mupperlim[i],plot,floc,dloc))
  else:
    temp = [en_extra_err (fi,mlowerlim,mupperlim,plot,floc,dloc) for fi in files]
  Es,errs = map(list,zip(*temp))
  Lxs = [discwt.getLxLyU(fi)[0] for fi in files]
  Ly = discwt.getLxLyU(files[0])[1]

  print ('---- Ly =',Ly,'----')
  print ('fitting with E vs. Lx:')
  print ('Lx E  E/Lx  E/N  err/N')
  for i in xrange(len(Es)):
    print (Lxs[i], Es[i], Es[i]/float(Lxs[i]), Es[i]/float(Lxs[i]*Ly), errs[i]/float(Lxs[i]*Ly))
  print ('\n')

  # extroplate E/N with 1/Lx
  x = [1/float(Li) for Li in Lxs]
  y = [Ei/float(Li*Ly) for Ei,Li in zip(Es,Lxs)]
  e = [ei/float(Li*Ly) for ei,Li in zip(errs,Lxs)]
  fit = np.polyfit(x,y,fitorder)
  ferr = fiterr (x,y,e,fitorder)
  print ('E/N =',fit[-1])
  print ('errorbar by random =', ferr)

  def fitf(x): return ff.polyf (fit,x)
  var = 0
  for xi,yi in zip(x,y):
    var += (yi-fitf(xi))**2
  print ('errorbar by variance =', var**0.5)

  if plot:
    pl.figure()
    pl.errorbar(x,y,e,marker='o',c='k')
    print ('fitted coefficients:\n', fit[::-1])
    print ('error =', ferr,'\n')
    def fitf(x): return ff.polyf (fit,x)
    fitx,fity = x+[0], map(fitf,x+[0])
    pl.plot(fitx,fity,c='r')
    pl.text (0.1,0.9,ff.fitfstr(fit),fontsize=20,transform=pl.gca().transAxes)
    pl.xlabel ('1/Lx',fontsize=20)
    pl.ylabel ('E/N',fontsize=20)
    title = 'ly'+str(Ly)+'.'+files[0][files[0].find('U'):].rstrip('.out')
    pl.title (title,fontsize=20)
    if plot == 2 or plot==3:
      pl.savefig (floc+'/'+title+'.extrapx.pdf')
      writefile (dloc+'/'+title+'.extrapx.dat',[x,y,e])
      writefile (dloc+'/'+title+'.extrapx.fit.dat',[fitx,fity])
    if plot == 1 or plot==3: pl.show()
    pl.close()
  ind = Lxs.index(max(Lxs))
  return fit[-1], max([ferr,e[ind]]) # should know how to estimate the errorbar here

def fiterr (x,y,e,order,n=1000):
  yex,summ,sum2 = [],0.,0.
  for i in range(n):
    yr = [rand.gauss(yi,ei) for yi,ei in zip(y,e)]
    fit = np.polyfit(x,yr,order)
    yex.append (fit[-1]) # extrapolated y
    summ += fit[-1]
    sum2 += fit[-1]*fit[-1]
  #print sum2/float(n) - (summ/float(n))**2
  sigma = sum2/float(n) - (summ/float(n))**2
  if abs(sigma) < 1e-12: return 1e-6
  else: return sqrt(sigma)

def en_extra_err (filename,mlowerlim=0,mupperlim=1000000000,plot=1,floc='.',dloc='.'):
  # get data of total energy
  dat = discwt.getdata (filename)
  dat = discwt.drop_small_m (dat,mlowerlim,mupperlim)
  E,err = discwt.energy_and_err (dat)
  mm = map(list,zip(*dat))[3]
  (Lx,Ly,U) = discwt.getLxLyU (filename)

  print ('*** Lx, Ly =',Lx,Ly,'***')
  print ('energy and error to be fitted: E  E/N  err  m')
  for i in xrange(len(E)):
    print (E[i], E[i]/float(Lx*Ly), err[i], int(mm[i]))

  # fit data
  fit = np.polyfit(err,E,1,w=np.array(err)**(-1))
  def fitf(x): return ff.polyf (fit,x)
  print ('fitting coefficient: ')
  print (fit[::-1])
  print ('error:', 0.2*abs(fit[-1]-min(E)),'\n')
  # plot
  if plot:
    pl.figure()
    pl.plot (err,E,marker='o',c='k')
    fitx,fity = err+[0], map(fitf,err+[0])
    pl.plot (fitx,fity,c='r')
    pl.text (0.1,0.9,ff.fitfstr(fit),fontsize=18,transform=pl.gca().transAxes)
    pl.text (0.1,0.8,'$m='+str(int(mm[-1]))+'$',fontsize=18,transform=pl.gca().transAxes)
    pl.xlabel ('trancation error',fontsize=20)
    pl.ylabel ('E',fontsize=20)
    title = filename.lstrip('huben').rstrip('edgeh.out')
    pl.title (title,fontsize=20)
    pl.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    if plot == 2 or plot==3:
      pl.savefig (floc+'/'+filename.rstrip('.out')+'.extraperr.pdf')
      writefile (dloc+'/'+filename.rstrip('.out')+'.extraperr.dat',[err,E])
      writefile (dloc+'/'+filename.rstrip('.out')+'.extraperr.fit.dat',[fitx,fity])
    if plot == 1 or plot==3: pl.show()
    pl.close()
  return fit[-1], 0.2*abs(fit[-1]-min(E))


#main ()
