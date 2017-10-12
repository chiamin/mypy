import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor')
sys.path.append ('/home/chiamin/Projects/code/code_ED/python')
from cmath import exp, pi, sin, cos
from hsz import file_get
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pylab as pl
import tight_binding as tb
from numpy.linalg import eigh

def extract_parentheses (s,typ=int):
  s = s.strip('():')
  s = s.split(',')
  x,y = map(typ,s)
  return x,y


def read_cc (fname,spin):
  cc = []
  key = '<c'+spin+'+ c'+spin+'>:'
  f = open (fname)
  for line in f:
    if key in line:
      tmp = line.split()
      x1,y1 = extract_parentheses (tmp[2])
      x2,y2 = extract_parentheses (tmp[4])
      val = float(tmp[-1])
      cc.append ([x1,y1,x2,y2,val])
  f.close()
  #for i in cc: print i
  return cc

def read_det (f,key):
    for line in f:
        if key in line:
            mat = []
            for line in f:
                if line == '\n':
                    return mat
                row = map(float,line.strip('|\n').split())
                mat.append (row)

def comb_ind (x,y,lx,ly):
  return (x-1)*ly+(y-1)
def split_ind (i,lx,ly):
  return i/ly+1, i%ly+1

def print_table (lx,ly):
  n = lx*ly
  for i in xrange(n):
    x,y = split_ind (i,lx,ly)
    print i,x,y

def corrmat (fname,lx,ly,spin):
  N = lx*ly
  cor = np.matrix (np.zeros((N,N)))
  cc = read_cc (fname,spin)
  for ci in cc:
    x1,y1,x2,y2,val = ci
    i = comb_ind (x1,y1,lx,ly)
    j = comb_ind (x2,y2,lx,ly)
    
    cor[i,j] = val
  return cor

def get_occ (fname):
  f = open (fname)
  f,lx = file_get (f,'lx =',int)
  f,ly = file_get (f,'ly =',int)
  f.close()

  corr_up = corrmat (fname,lx,ly,'up')
  corr_dn = corrmat (fname,lx,ly,'dn')
  corr = corr_up + corr_dn
  val,vec = np.linalg.eigh (corr)
  val = val[::-1] # reverse the order
  vec = vec.transpose()
  vec = vec[::-1]

  return val, vec, lx,ly

def np_fft (f,lx,ly):
  f = np.reshape (f,(lx,ly))
  # the first index is for lx; the second is for ly
  fq = np.fft.fftn (f)
  fq = fq.reshape(-1,).tolist()
  qx = 2.*pi*np.fft.fftfreq (lx)
  qy = 2.*pi*np.fft.fftfreq (ly)

  spe = [v.real**2 + v.imag**2 for v in fq]
  return qx,qy,spe

def fourier_transform (fs,xs,qs):
  fqs = []
  for q in qs:
    fq = 0.+0j
    for i in xrange(len(fs)):
      x = xs[i]
      f = fs[i]
      fq += exp (-1j*q*x) * f
    fqs.append (fq)
  return fqs

def plot_each (qx,qy,fq):
  lx,ly = len(qx),len(qy)
  fq = np.reshape (fq,(lx,ly))
  fq = fq.transpose().tolist()

  pl.figure()
  markers=['o', 'x', '^', 's', 'd', 'v']
  for fi,qyi,mk in zip(fq,qy,markers):
    pl.plot (qx,fi,mk+'-',ms=10,alpha=.5,label='qy='+str(qyi))
  pl.legend()

def get_qxy (qx,qy):
  qxy = []
  for qxi in qx:
    for qyi in qy:
      qxy.append ([qxi,qyi])
  return qxy

def sortq (qx,qy,fq):
# Sort [qx,qy] based on fq
  qxy = get_qxy (qx,qy)
  tmp = zip(fq,qxy)
  tmp.sort(reverse=True)
  sfq,sqxy = zip(*tmp)
  return sfq, sqxy

def analysis_q (orb,lx,ly,doplot=False):
  # Plot the orbital
  if doplot:
    plot_each (range(lx),range(ly),orb)

  # Fourier transform the orbital
  qx,qy,fq = np_fft (orb,lx,ly)

  # Plot the orbital in q-space
  if doplot:
    plot_each (qx,qy,fq)
    pl.show()

  # Select the qx and qy 
  sfq, sqxy = sortq (qx,qy,fq)
  qxys = [sqxy[0]]

  # Add -qx and -qy
  qx,qy = sqxy[0]
  if qx != 0: qxys.append ([-qx,qy])
  if qy != 0: qxys.append ([qx,-qy])
  if qx != 0 and qy != 0: qxys.append ([-qx,-qy])

  return qxys

def tight_binding (lx,ly,Np,tx,ty,pbcx,pbcy):
  H = tb.H_K (lx,ly,tx,ty,0.,pbcx,pbcy)
  E, U = eigh (H) # The column U[:, i] is the normalized eigenvector corresponding to the eigenvalue E[i]
  vecs = U.transpose()
  occs = [1]*Np+[0]*(lx*ly-Np)
  return occs, vecs

def plot_occ_scatter (occq_dict):
# Scatter-plot of occup(qx,qy)
  occs = occq_dict.values()
  qxys = occq_dict.keys()
  qxs,qys = zip(*qxys)

  fig = pl.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter (qxs,qys,occs)

  return qxs,qys,occs

def get_occq_dict (occs, orbs):
  occq_dict = dict()
  for occ,orb in zip(val,vec):
    qxys = analysis_q (orb,lx,ly)
    for qx,qy in qxys:
      occq_dict[qx,qy] = occ
  return occq_dict

def plot_occ_contour (qxs,qys,occq_dict):
  qxset,qyset = set(qxs),set(qys)
  qx,qy = list(qxset),list(qyset)
  qx.sort()
  qy.sort()
  occs = []
  for qyi in qy:
    occs.append([])
    for qxi in qx:
      try:
        occ = occq_dict[qxi,qyi]
      except KeyError:
        occ = float('Nan')
      occs[-1].append (occ)

  [X,Y] = np.meshgrid (qx,qy)
  pl.figure()
  pl.contourf (X,Y,occs)
  pl.colorbar()


if __name__ == '__main__':

  fname = sys.argv[1]
  val,vec,lx,ly = get_occ (fname)
  #print_table (lx,ly)

  '''
  # Tight binding test
  lx,ly,tx,ty,pbcx,pbcy = 16,4,1.,1.,False,True
  Np = lx*ly/2
  val, vec = tight_binding (lx,ly,Np,tx,ty,pbcx,pbcy)
  '''

  # Get occupations as a dictionary of (qx,qy)
  occq_dict = get_occq_dict (val,vec)

  qxs,qys,occs = plot_occ_scatter (occq_dict)

  plot_occ_contour (qxs,qys,occq_dict)

  pl.show()
