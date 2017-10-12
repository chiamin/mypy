import sys
sys.path.append ('/home/bluewhite/Projects/mypy')
sys.path.append ('/home/bluewhite/Projects/mypy/dmrg')
from CMC_file import *
import pylab as pl
import numpy as np
import get_nnwt as discwt
import fitfun as ff
import random as rand
from math import sqrt

def en_extra_x (files,mlowerlim=0,mupperlim=sys.maxint,fitorder=2,plot=True,mfitorder=1):
  # get non-error energies
  if type(mlowerlim)==list:
    temp = []
    for i in xrange(len(files)):
      temp.append (nn_extra_err (files[i],mlowerlim[i],mupperlim[i],plot,mfitorder))
  else:
    temp = [nn_extra_err (fi,mlowerlim,mupperlim,plot,mfitorder) for fi in files]
  nns,errs = map(list,zip(*temp))
  Lxs = [discwt.getLxLyU(fi)[0] for fi in files]
  Ly = discwt.getLxLyU(files[0])[1]

  print '---- Ly =',Ly,'----'
  print 'fitting with nn vs. Lx:'
  print 'nup*ndown  Lx'
  for i in xrange(len(nns)):
    print nns[i], Lxs[i]
  print '\n'

  # extroplate nn/N with 1/Lx
  x = [1/float(Li) for Li in Lxs]
  y = nns
  e = errs
  fit = np.polyfit(x,y,fitorder)
  ferr = ff.fiterr (x,y,e,fitorder)
  print 'fitted coefficients:\n', fit[::-1]
  print 'errorbar by random =', ferr

  def fitf(x): return ff.polyf (fit,x)
  var = 0
  for xi,yi in zip(x,y):
    var += (yi-fitf(xi))**2
  print 'errorbar by variance =', var**0.5,'\n'

  if plot:
    pl.figure()
    pl.errorbar(x,y,e,marker='o',c='k')
    def fitf(x): return ff.polyf (fit,x)
    fitx,fity = x+[0], map(fitf,x+[0])
    pl.plot(fitx,fity,c='r')
    pl.text (0.1,0.9,ff.fitfstr(fit),fontsize=20,transform=pl.gca().transAxes)
    pl.xlabel ('1/Lx',fontsize=20)
    pl.ylabel ('nn/N',fontsize=20)
    title = 'ly'+str(Ly)+'.'+files[0][files[0].find('U'):].rstrip('.out')
    pl.title (title,fontsize=20)
    #if plot == 2 or plot==3:
    #  pl.savefig ('../fig/'+title+'.nn.extralx.pdf')
    #  writefile ('../plotdat/'+title+'.nn.extralx.dat',[x,y,e])
    #  writefile ('../plotdat/'+title+'.nn.extralx.fit.dat',[fitx,fity])
    if plot == 1 or plot==3: pl.show()
    pl.close()
  ind = Lxs.index(max(Lxs))
  return fit[-1], max([ferr,e[ind]]) # should know how to estimate the errorbar here

def fiterr (x,y,e,order,n=200):
  yex,summ,sum2 = [],0.,0.
  for i in range(n):
    yr = [rand.gauss(yi,ei) for yi,ei in zip(y,e)]
    fit = np.polyfit(x,yr,order)
    yex.append (fit[-1]) # extrapolated y
    summ += fit[-1]
    sum2 += fit[-1]*fit[-1]
  return sqrt(sum2/float(n) - (summ/float(n))**2)

def nn_extra_err (filename,mlowerlim=0,mupperlim=sys.maxint,plot=True,fitorder=1):
  # get data of total energy
  dat = discwt.getdata (filename)
  dat = discwt.drop_small_m (dat,mlowerlim,mupperlim)
  nn,err = discwt.nn_and_err (dat)
  mm = map(list,zip(*dat))[3]
  (Lx,Ly,U) = discwt.getLxLyU (filename)

  print '*** Lx, Ly =',Lx,Ly,'***'
  print 'nup*ndown and error to be fitted: nn  err  m'
  for i in xrange(len(nn)):
    print nn[i], err[i], int(mm[i])
    err[i] = err[i]**fitorder
  # fit data
  #err = [i**2 for i in err]
  fit = np.polyfit(err,nn,1,w=np.array(err)**(-1))
  def fitf(x): return ff.polyf (fit,x)
  print 'fitting coefficient: '
  print fit[::-1]
  print 'error:', 0.2*abs(fit[-1]-min(nn)),'\n'
  # plot
  if plot:
    pl.figure()
    pl.plot (err,nn,marker='o',c='k')
    fitx,fity = err+[0], map(fitf,err+[0])
    pl.plot (fitx,fity,c='r')
    pl.text (0.1,0.9,ff.fitfstr(fit),fontsize=20,transform=pl.gca().transAxes)
    pl.xlabel ('trancation error',fontsize=20)
    pl.ylabel ('$\langle n_\uparrow n_\downarrow \\rangle$',fontsize=20)
    title = filename.lstrip('huben').rstrip('edgeh.out')
    pl.title (title,fontsize=20)
    pl.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #if plot == 2 or plot==3:
    #  pl.savefig ('../fig/'+filename.rstrip('.out')+'.nn.extraerr.pdf')
    #  writefile ('../plotdat/'+filename.rstrip('.out')+'.nn.extraerr.dat',[err,nn])
    #  writefile ('../plotdat/'+filename.rstrip('.out')+'.nn.extraerr.fit.dat',[fitx,fity])
    if plot == 1 or plot==3: pl.show()
    pl.close()
  return fit[-1], 0.2*abs(fit[-1]-min(nn))


#main ()
