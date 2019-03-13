import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import imp
import pylab as pl

ut = imp.load_source ('ut','/home/chiamin/mypy/dmrg.itensor/utility.py')

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

def plotn (fname,ax=0,c='k',plotmux=1,y=1,lb='',mk='o',mfc='',mks=6):
    if len(sys.argv) > 2: SWP = sys.argv[2]
    else: SWP = 0

    lx,ly = ut.getLxy (fname)
    if plotmux: gg,mu,gg = get_mu (fname)

    Ns,swps,ms = [],[],[]
    f = open (fname)
    while 1:
        try:
            if SWP == 0:
                f,swp,m,xs,ys,nups,ndns,ns,szs,hs = ut.get_meas (f,lx,ly)
            else:
                f,swp,m,xs,ys,nups,ndns,ns,szs,hs = ut.get_meas (f,lx,ly,SWP)
                break
        except KeyError:
            break

    x = range(1,lx+1)
    n = []
    for xi in x:
        i = xs.index(xi)
        n.append (nups[i] + ndns[i])
    if plotmux: x = mu

    #for xi,ni in zip(x,n): print xi,ni

    mew = 1
    if mk=='x': mew = 2
    if mfc=='': mfc = c
    if ax:
        ax.plot (x,n,'o-',c=c,label=lb,marker=mk,mew=mew,mfc=mfc,ms=mks)
    else:
        #print len(x),len(n)
        pl.plot (x,n,'o-',c=c,label=lb,marker=mk,mew=mew,mfc=mfc,ms=mks)
    #pl.show()
    return x,n

if __name__ == '__main__':
    fname = sys.argv[1]
    plotn (fname,plotmux=0)
    pl.show()
