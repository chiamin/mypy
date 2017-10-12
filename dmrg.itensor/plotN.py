import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut
import pylab as pl

if __name__ == '__main__':
    fname = sys.argv[1]
    lx,ly = ut.getLxy (fname)

    Ns,swps,ms = [],[],[]
    f = open (fname)
    while 1:
        try:
            f,swp,m,xs,ys,nups,ndns,ns,szs,hs = ut.get_meas (f,lx,ly)
            Ns.append (sum(ns))
            swps.append (swp)
            ms.append (m)
        except KeyError:
            break

    #print swps
    for i in xrange(1,len(swps)):
        if swps[i] < swps[i-1]: break
    print 'm=',ms[i:]
    pl.plot (swps[i:],Ns[i:],'o-')
    pl.show()
