import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut
import pylab as pl
import utility_mmu as utmm

def get_mu (fname,y=1):
    f = open (fname)
    for line in f:
        if 'x' in line and 'y' in line and 'mu' in line and 'h' in line:
            break
    xs,mus,hs = [],[],[]
    for line in f:
        if '}' in line: break
        tmp = line.split()
        xi,yi,mu,h = int(tmp[0]),int(tmp[1]),float(tmp[2]),float(tmp[3])
        if yi == y:
            xs.append (xi)
            mus.append (mu)
            hs.append (h)
    return xs,mus,hs

if __name__ == '__main__':
    fname = sys.argv[1]
    y = 1
    plotmu = 0

    lx,ly = ut.getLxy (fname)
    if plotmu: gg,mu,gg = get_mu (fname)

    mus = utmm.get_mus (fname)
    N_state = len(mus)

    Ns,swps,ms = [],[],[]
    f = open (fname)
    while 1:
        try:
            f,swp,m,xs,ys,nups,ndns,ns,szs,hs = utmm.get_meas_multi_states (f,lx,ly,N_state)
        except KeyError:
            break

    x = range(1,lx+1)
    for ist in xrange(len(mus)):
        n = []
        for xi in x:
            i = xs[ist].index(xi)
            n.append (nups[ist][i] + ndns[ist][i])

        pl.plot (x,n,'o-',label='mu='+str(mus[ist]))

    pl.legend()
    pl.show()
