import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor')
import imp
import pylab as pl
import plotn

ut = imp.load_source ('ut','/home/chiamin/mypy/dmrg.itensor/utility.py')

def get_pairing (fname):
    f = open (fname)
    swps,ms,delta_dicts = [],[],[]
    EOF = False
    for line in f:
        if 'Sweep=' in line:
            swp = int(line.split(',')[0].split('=')[-1])
        elif 'Max_m=' in line:
            m = int(line.split('=')[-1])
        elif 'Pairing:' in line:
            delta_dict = dict()
            for line in f:
                if 'CPU' in line:
                    swps.append (swp)
                    ms.append(m)
                    delta_dicts.append (delta_dict)
                    break
                tmp = line.split()
                x1,y1,x2,y2 = map(int,tmp[:4])
                di = float(tmp[-1])
                delta_dict[x1,y1,x2,y2] = di
    delta_dicts.append (delta_dict)
    return swps,ms,delta_dicts

def print_pairing_x (fname,y=1,ax=0,plotmux=1):
    swps,ms,delta_dicts = get_pairing (fname)
    delta_dict = delta_dicts[-1] # delta_dict[x1,y1,x2,y2] = delta

    lx,ly = ut.getLxy (fname)
    xs = range(1,lx+1)
    if y == ly: y2 = 1
    else: y2 = y+1
    deltax = [delta_dict[x,y,x+1,y] for x in xs[:-1]]
    deltay = [delta_dict[x,y,x,y2] for x in xs]

    gg,mu,gg = plotn.get_mu (fname)
    if plotmux: xs = mu

    if ax:
        ax.plot (xs[:-1],deltax,'o-k',ms=4)
        ax.plot (xs,deltay,'o-k',ms=4)
    else:
        pl.plot (xs[:-1],deltax,'o-k',ms=4)
        pl.plot (xs,deltay,'o-k',ms=4)
    #pl.yscale('log')
    #pl.show()

if __name__ == '__main__':
    print_pairing_x (sys.argv[1])
    pl.show()
