import sys, re
sys.path.append ('/home/bluewhite/Projects/mypy')
sys.path.append ('/home/bluewhite/Projects/mypy/dmrg')
from CMC_file import *
import pylab as pl
import numpy as np
import subprocess as sp
import get_discwt as discwt
import fitfun as ff

#files1 = ['huben16x3.U12.n1.tp0.edgeh.out','huben32x3.U12.n1.tp0.edgeh.out']
#files2 = ['huben16x4.U12.n1.tp0.edgeh.out','huben32x4.U12.n1.tp0.edgeh.out']
#files3 = ['huben14x5.U12.n1.tp0.edgeh.out','huben20x5.U12.n1.tp0.edgeh.out']
#write = True
#plot = True

def extra_check ():
  files1 = ['huben12x3.U8.n1.tp0.edgeh.out','huben16x3.U8.n1.tp0.edgeh.out']
  files2 = ['huben16x3.U8.n1.tp0.edgeh.out','huben32x3.U8.n1.tp0.edgeh.out']
  E1 = en_diff_extra (files1[0],files1[1],500,plot=plot)
  E2 = en_diff_extra (files2[0],files2[1],500,plot=plot)
  pl.show()

def en_diff_extra_2 (files,mlowerlim=0,mupperlim=sys.maxint,write=True,plot=True):
  E1,e1 = en_diff_extra (files[0:2],mlowerlim,mupperlim,write,plot)
  E2,e2 = en_diff_extra (files[1:],mlowerlim,mupperlim,write,plot)
  Lx1,Ly1,U1 = discwt.getLxLyU (files[1])
  Lx2,Ly2,U2 = discwt.getLxLyU (files[2])
  print 'E ='
  print Lx1,E1,e1
  print Lx2,E2,e2
  print 'difference =', E1-E2, e1+e2, '\n'
  fitE,fiterr = ff.polyfiterr ([1/float(Lx1),1/float(Lx2)],[E1,E2],[e1,e2],1,plot=plot)
  print 'extrap E =',fitE,'+-',fiterr
  #if plot:
  #Lx1,Ly1,U1 = discwt.getLxLyU (files[0])
  #Lx2,Ly2,U2 = discwt.getLxLyU (files[1])
  #Lx3,Ly3,U3 = discwt.getLxLyU (files[2])
  #x,y,e = [1/float(Lx3-Lx1),1/float(Lx3-Lx2)],[E1,E2],[e1,e2]
  #pl.errorbar (x,y,e,marker='o',c='k')
  #return E2,e2
  return fitE, fiterr

def en_diff_extra (files,mlowerlim=0,mupperlim=sys.maxint,write=True,plot=True):
  # get total E
  dat1 = discwt.getdata (files[0])
  dat2 = discwt.getdata (files[1])
  dat1 = discwt.drop_small_m (dat1,mlowerlim,mupperlim)
  dat2 = discwt.drop_small_m (dat2,mlowerlim,mupperlim)
  print files[0],files[1]
  Lx1,Ly1,U1 = discwt.getLxLyU (files[0])
  Lx2,Ly2,U2 = discwt.getLxLyU (files[1])
  if Ly1 != Ly2:
    print 'Error: Ly1 and Ly2 should be equal.'
    exit()
  # substract energy; get E/N
  Ediff, err, mm = subenergy (dat1, dat2, Lx1,Lx2,Ly1)
  #if dellast: del Ediff[-1], err[-1], mm[-1]
  fit = np.polyfit (err,Ediff,1,w=np.array(err)**(-1))
  print 'fitted coefficients:\n', fit[::-1]

  # plot
  if plot:
    pl.figure()
    pl.plot (err,Ediff,marker='o',c='k')
    fitf = np.poly1d(fit)
    fitx,fity = np.insert(err,0,0),fitf(np.insert(err,0,0))
    pl.plot (fitx,fity,c='r')
    pl.text (0.1,0.8,ff.fitfstr(fit),fontsize=20,transform=pl.gca().transAxes)
    pl.xlabel ('truncated weight',fontsize=20)
    pl.ylabel ('E/N',fontsize=20)
    title = str(Lx2)+'_'+str(Lx1)+'x'+str(Ly1)+'.'+files[0][files[0].find('U'):].rstrip('.out')
    pl.title (title,fontsize=20)
    if plot==1 or plot==3: pl.show()
    elif plot==2 or plot==3:
      pl.savefig ('../fig/'+title+'.diffextraerr.pdf')
      pl.close()
      writefile ('../plotdat/'+title+'.diffextraerr.dat',[err,Ediff])
      writefile ('../plotdat/'+title+'.diffextraerr.fit.dat',[fitx,fity])
  return fit[-1], 0.2*abs(fit[-1]-min(Ediff))

def subenergy (data1, data2, Lx1, Lx2, Ly):
  Ediff,err,mm = [],[],[]
  print 'm E1 E2'
  for di1,di2 in zip(data1,data2):
    if di1[3] == di2[3]:
      Ediff.append ( (di2[1]-di1[1]) / ((Lx2-Lx1)*Ly) )
      err.append (di1[2]+di2[2])
      mm.append (di1[3])
      print di1[3], di1[1], di2[1]
    prem = di1[3]
  return Ediff, err, mm
