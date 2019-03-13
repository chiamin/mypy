import sys, os
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import pylab as pl
import trunerr as te
import utility as ut
from kagomeXC_diamond import get_kagome

def ferro_order (sz,links,lx,ly,xskip=0):
    mags = []
    for i,j in links:
        mags.append (sz[i] * sz[j])
    return sum(mags)/float(len(mags))

def get_ferro (fname,xskip=0):
    sweeps, cutoffs, ms, terr, E, Eps = te.trunerr2 (fname,verbose=False)
    mags = []
    with open(fname) as f:
        for line in f:
            if 'Lx =' in line: lx = int(line.split()[-1])
            elif 'Ly =' in line: ly = int(line.split()[-1])
            elif 'periodic_x' in line: xpbc = int(line.split()[-1])
            elif 'periodic_y' in line: ypbc = int(line.split()[-1])
            elif '}' in line: break

        links, units, N = get_kagome (lx,ly,xpbc,ypbc)

        for swp,m,ti in zip(sweeps,ms,terr):
            f,swp,m,obss = ut.get_meas_obs (f,N,['Sz ='],sweep=swp)
            sz = obss[0]
            mags.append (ferro_order (sz,links,lx,ly,xskip=xskip))
    return mags[-1]
