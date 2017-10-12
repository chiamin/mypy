import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import utility as ut
import pylab as pl
import utility_mmu as utmm

if __name__ == '__main__':
    fname = sys.argv[1]
    y = 1

    lx,ly = ut.getLxy (fname)
    x = range(1,lx+1)

    mus = utmm.get_mus (fname)
    N_state = len(mus)

    for ist in xrange(len(mus)):

        f = open (fname)
        while 1:
            try:
                f,swp,m,delta_dict = ut.get_pairing (f,key='Pairing , State '+str(ist))    # delta_dict[x1,y1,x2,y2] = delta
            except EOFError:
                break

        print ist,swp,m,delta_dict[1,1,1,2]

        delta_x, delta_y = [],[]
        for xi in x:
            if xi == x[-1]:
                dix = float('Nan')
            else:
                dix = delta_dict[xi,y,xi+1,y]

            if y == ly:
                diy = delta_dict[xi,y,xi,1]
            else:
                diy = delta_dict[xi,y,xi,y+1]

            delta_x.append (dix)
            delta_y.append (diy)

        p = pl.plot (x,delta_x,'o-',label='mu='+str(mus[ist]))
        pl.plot (x,delta_y,'x-',c=p[0].get_color())

    pl.legend()
    pl.show()
