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
from matplotlib.mlab import griddata

def plot_3d (z,x,y,title=''):
    lx,ly = len(x),len(y)
    Z = np.reshape (z,(lx,ly))

    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')
    Y,X = np.meshgrid(y,x)
    surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    pl.title(title)

def plot_orb_slice (orb,lx,ly,title=''):
    orb = np.reshape (orb,(lx,ly))
    pl.figure()
    for yi in xrange(ly):
        orbx = orb[:,yi]      # orbital alogn x for y=yi
        pl.plot (orbx,'o-',label='y='+str(yi))
        break
    pl.xlabel('x',fontsize=18)
    #pl.legend()
    pl.title(title)
    pl.figure()
    for xi in xrange(0,lx*ly,ly):
        orby = orb[xi,:]    # orbital alogn y for x=xi
        pl.plot (orby.T,'o-',label='x='+str(xi))
        break
    pl.xlabel('y',fontsize=18)
    #pl.legend()
    pl.title(title)

def read_det (f,key):
    for line in f:
        if key in line:
            #print 'Got',key
            mat = []
            for line in f:
                if line == '\n':
                    return mat
                row = map(float,line.strip('|\n').split())
                mat.append (row)
    raise KeyError

def get_nat_orbs (fname):
    f = open (fname)
    
    corr_up = read_det (f,'correlation matrix up')
    corr_dn = read_det (f,'correlation matrix dn')
    corr_up = np.matrix(corr_up)
    corr_dn = np.matrix(corr_dn)
    corr = corr_up + corr_dn
    
    #corr = np.matrix (read_det (f,'correlation matrix'))

    occ,orbs = np.linalg.eigh (corr)
    # Note that orbitals are stored in columns, not rows
    return occ, orbs

def find_q_1d (orb,apbc=False):
    if apbc:
    # extend the orbital to 2*L
        #pl.plot (orb,'o-k')

        orb = np.array(orb)
        invorb = -orb
        orb = np.append (orb,invorb)

        #pl.plot (orb,'x-r')
        #pl.show()

    fq = np.fft.fftn (orb)
    pow_spec = np.abs(fq)
    qs = 2.*np.fft.fftfreq (len(orb)) # in the unit of pi
    # find k of maximum amplitude
    maxi  = np.argmax(pow_spec)

    return qs[maxi], fq[maxi]

def find_qxy_from_1d (orb,lx,ly,apbc=False):
# Have assumed that only one qx and one qy are significant
    '''
    for xi in xrange(0,lx*ly,ly):
        print 'xi=',xi
        orby = orb[xi:xi+ly]
        if apbc:
            pl.plot (orby,'o-k')
            orby = np.array(orby)
            invorb = -orby
            orby = np.append (orby,invorb)
            pl.plot (orby,'x-r')
    pl.show()
    '''

    xi,yi = lx/2,ly/2    # take the center lines
    orb = np.reshape(orb,(lx,ly))
    orbx = orb[:,yi]      # orbital alogn x for y=yi
    orby = orb[xi,:].T    # orbital alogn y for x=xi

    qx,fqx = find_q_1d (orbx)
    qy,fqy = find_q_1d (orby,apbc)
    return qx,qy,[fqx,fqy]

def find_qxy (orb,lx,ly,apbcy=False):
    if apbcy:
    # extend the orbital to 2*L
        orb = np.reshape (orb,(lx,ly))
        orb = np.array(orb)
        invorb = -orb
        orb = np.append (orb,invorb,1)
        ly = 2*ly
    
    orb = np.reshape (orb,(lx,ly))
    fq = np.fft.fft2 (orb)

    pow_spec = np.abs(fq)**2
    qxs = 2.*np.fft.fftfreq (lx) # in the unit of pi
    qys = 2.*np.fft.fftfreq (ly) # in the unit of pi
    psmax = max(np.reshape(pow_spec,(-1,)))
    imax = np.where(pow_spec==psmax)
    xi,yi = imax[0][0],imax[1][0]
    return qxs[xi], qys[yi], fq[xi,yi]

def check_periodic (f):
# Check if the (1D) function f is periodic or anti-periodic. Typically for open-boundary system.
    f = np.array(f)
    fmap1 = f[::-1]
    fmap2 = -(f[::-1])
    s1 = sum(np.abs(f+fmap1))
    s2 = sum(np.abs(f+fmap2))
    return s1 < s2

def extend_anti_x (orb,lx,ly):
# Extend the orbital to double length in x direction, assuming anti-periodic.
    orb = np.reshape (orb,(lx,ly))
    invorb = -orb
    orb = np.concatenate ((orb,invorb),axis=0)
    lx = 2*lx
    return orb

def check_periodic_x (orb,lx,ly,x=0):
    orb = np.reshape (orb,(lx,ly))
    return check_periodic (orb[:,x])

def get_occ_q_dict (occs,orbs,lx,ly,apbc=False):
    occq_dict = dict()
    occq_dup_dict = dict()
    orb_dict  = dict()
    fq_dict   = dict()
    ind_dict  = dict()
    #for i in xrange(len(occs)):
    for i in xrange(-1,-len(occs)-1,-1):
        lxi,lyi = lx,ly
        occ,orb = occs[i],orbs[:,i]
        # If orbital is anti-periodic in x-direction, extend to double length
        if not check_periodic_x (orb,lx,ly):
            orb = extend_anti_x (orb,lx,ly)
            lxi,lyi = orb.shape
        # Get qx,qy
        qx,qy,fq = find_qxy (orb,lxi,lyi,apbc)
        # Check not duplicate
        if (qx,qy) in occq_dict and occ != occq_dict[qx,qy]:
            print 'duplicate k:(',qx,qy,'), occ =',occq_dict[qx,qy],occ#,'|',np.abs(fq_dict[qx,qy]),np.angle(fq_dict[qx,qy]),',',np.abs(fq),np.angle(fq)
            occq_dup_dict[qx,qy] = occ
            '''
            plot_3d (orb_dict[qx,qy],range(lxi),range(lyi),title='old')
            plot_orb_slice (orb_dict[qx,qy],lxi,lyi,title='old')
            plot_3d (orb,range(lxi),range(lyi),title='new')
            plot_orb_slice (orb,lxi,lyi,title='new')
            pl.show()
            '''
            orb_old = np.reshape (orb_dict[qx,qy],(lxi,lyi))
            orb_new = np.reshape (orb,(lxi,lyi))
            fq_old = np.fft.fft2 (orb_old)
            fq_new = np.fft.fft2 (orb_new)
            qxs = 2.*np.fft.fftfreq (lxi) # in the unit of pi
            qys = 2.*np.fft.fftfreq (lyi) # in the unit of pi
            print 'fq =',abs(fq_dict[qx,qy])**2,abs(fq)**2
            print 'old'
            sq_old = np.abs(fq_old)**2
            for i in xrange(len(qxs)):
                for j in xrange(len(qys)):
                    qxi,qyi = qxs[i],qys[j]
                    sq = abs(fq_old[i,j])**2
                    if sq > 2: print qxi,qyi,sq
            print 'new'
            for i in xrange(len(qxs)):
                for j in xrange(len(qys)):
                    qxi,qyi = qxs[i],qys[j]
                    sq = abs(fq_new[i,j])**2
                    if sq > 2: print qxi,qyi,sq
            '''plot_3d (fq_old,range(fq_old.shape[0]),range(fq_old.shape[1]),title='old')
            plot_3d (fq_new,range(fq_new.shape[0]),range(fq_new.shape[1]),title='new')
            pl.show()'''
            #if abs(occ - occq_dict[qx,qy]) > 4e-3: raise Exception
        else:
            occq_dict[qx,qy] = occ
            orb_dict[qx,qy]  = orb
            fq_dict[qx,qy]   = fq
            ind_dict[qx,qy]  = i
    # Set symmetry
    for qx,qy in occq_dict.keys():
        # Map to +-qx,+-qy
        if qx != 0: occq_dict[-qx,qy] = occq_dict[qx,qy]
        if qy != 0: occq_dict[qx,-qy] = occq_dict[qx,qy]
        if qx != 0 and qy != 0: occq_dict[-qx,-qy] = occq_dict[qx,qy]

    '''for qx,qy in occq_dup_dict.keys():
        if qx != 0: occq_dup_dict[-qx,qy] = occq_dup_dict[qx,qy]
        if qy != 0: occq_dup_dict[qx,-qy] = occq_dup_dict[qx,qy]
        if qx != 0 and qy != 0: occq_dup_dict[-qx,-qy] = occq_dup_dict[qx,qy]'''
    return occq_dict, ind_dict, occq_dup_dict

def plot_occ_scatter (occq_dict,title='',c='b',mk='o',ms=12,ax=None):
# Scatter-plot of occup(qx,qy)
    if ax is None:
        fig = pl.figure()
        ax = fig.add_subplot(111, projection='3d')

    occs = occq_dict.values()
    qxys = occq_dict.keys()
    qxs,qys = zip(*qxys)
    ax.scatter (qxs,qys,occs,c=c,marker=mk,s=ms)
    pl.title(title)
    pl.xlabel ('$k_x/\\pi$',fontsize=20)
    pl.ylabel ('$k_y/\\pi$',fontsize=20)
    ax.set_zlabel ('$\\langle n\\rangle_1$',fontsize=20)

    return qxs,qys,occs,ax

def plot_occ_contour (qxs,qys,occq_dict,title=''):
    fig = pl.figure()

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
                pass
                #occ = float('Nan')
            occs[-1].append (occ)
    [X,Y] = np.meshgrid (qx,qy)
    v = np.linspace(0., 2., 11, endpoint=True)
    pl.contourf (X,Y,occs,v)
    
    '''
    x,y,z = [],[],[]
    for qyi in qy:
        for qxi in qx:
            try:
                z.append (occq_dict[qxi,qyi])
                x.append (qxi)
                y.append (qyi)
            except KeyError:
                pass
    xi = np.linspace(min(x), max(x), 50)
    yi = np.linspace(min(y), max(y), 50)
    zi = griddata(x, y, z, xi, yi, interp='linear')
    pl.contourf (xi,yi,zi)
    '''

    pl.xlabel ('$k_x/\\pi$',fontsize=20)
    pl.ylabel ('$k_y/\\pi$',fontsize=20)
    cb = pl.colorbar(ticks=v)
    cb.ax.set_ylabel ('$\\langle n\\rangle_1$',fontsize=20)
    pl.title(title,fontsize=20)

    for qyi in qy:
        pl.plot (qx,[qy]*len(qx),'--k',c='k',lw=0.5)


def get_occ_q_dict_from_file (fname,lx,ly,apbc=False):
    occ,orbs  = get_nat_orbs (fname)
    occq_dict,ind_dict,occq_dup_dict = get_occ_q_dict (occ,orbs,lx,ly,apbc)
    return occq_dict

def symm_qxy (occq_dict):
    re = dict()
    for qx,qy in occq_dict:
        re[qy,qx] = occq_dict[qx,qy]
    return re

if __name__ == '__main__':
    fname = sys.argv[1]
    lx,ly = sys.argv[2],sys.argv[3]
    title, apbc = '',False
    for arg in sys.argv:
        if 'tit'   in arg: title = arg.split('=')[-1]
        if '-apbc' in arg: apbc = True

    occq_dict  = get_occ_q_dict_from_file (fpbc, lx,ly,apbc=False)

    qxs,qys,occs,ax   = plot_occ_scatter (occq_dict, c='b')

    plot_occ_contour (qxs,qys,occq_dict)

    pl.show()
