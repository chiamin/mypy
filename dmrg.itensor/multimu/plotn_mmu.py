import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut
import pylab as pl
import utility_mmu as utmm

if __name__ == '__main__':
    fname = sys.argv[1]
    y = 1

    lx,ly = ut.getLxy (fname)

    mus = utmm.get_mus (fname)
    N_state = len(mus)

    f = open (fname)
    while 1:
        try:
            f,swp,m,xs,ys,nups,ndns,ns,szs,hs = utmm.get_meas_multi_states (f,lx,ly,N_state)
        except KeyError:
            break

    print m

    ns = []
    for ist in xrange(len(mus)):
        N = sum(nups[ist]) + sum(ndns[ist])
        ns.append (N/(lx*ly))

    pl.plot (mus,ns,'o-')
    pl.xlabel ('mu',fontsize=16)
    pl.ylabel ('n',fontsize=16)

    pl.show()
