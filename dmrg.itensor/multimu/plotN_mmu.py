import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut
import pylab as pl
import utility_mmu as utmm

if __name__ == '__main__':
    fname = sys.argv[1]
    y = 1
    mmin = 7000

    lx,ly = ut.getLxy (fname)

    mus = utmm.get_mus (fname)
    N_state = len(mus)

    f = open (fname)
    while 1:
        try:
            f,swp,m,xs,ys,nups,ndns,ns,szs,hs = utmm.get_meas_multi_states (f,lx,ly,N_state)

            if m < mmin: continue
            print m

            ns = []
            for ist in xrange(len(mus)):
                N = sum(nups[ist]) + sum(ndns[ist])
                ns.append (N)

            pl.plot (mus,ns,'o-',label='m='+str(m))
        except KeyError:
            break


    pl.xlabel ('mu',fontsize=16)
    pl.ylabel ('n',fontsize=16)
    pl.legend (loc='upper left')
    pl.show()
