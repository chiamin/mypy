import sys, os, glob
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import pylab as pl
import trunerr as te
import utility as ut
from kagomeXC_diamond import get_kagome
from bond_en import get_SS
from plot_kagomeXC import plot_kagome_lattice as plot_kagome_latticeXC
from plot_kagomeYC import plot_kagome_lattice as plot_kagome_latticeYC
from matplotlib import rc, ticker, colors

def fformat (a):
    if abs(a) < 1e-5 or abs(a) > 1e5:
        return '{:.5e}'.format(a)
    else:
        return '{:.2g}'.format(a)

def plot_kagome_sz (ax, pos, f, swp, maxl=2, zerosz=1e-3, text_shift=3, fontsize=40, label=True):
    # get sz
    N = len(pos)
    f,swp,m,sites,obss = ut.get_meas_obs (f,N,['Sz ='],sweep=swp)
    sz = obss[0]

    def plot_arrow (ax, x, y, halfl, c):
        ax.arrow (x, y-halfl, dx=0, dy=2*halfl, width=0.05,length_includes_head=True,head_width=0.3,head_length=0.5*abs(halfl),fc=c,ec=c)
    # plot
    #print sz
    abssz = [abs(i) for i in sz]
    maxsz,minsz = max(abssz),min(abssz)
    fac = maxl/(maxsz-zerosz)
    fac = max(0,fac)
    for i in xrange(len(sz)):
        site = sites[i]-1
        x,y = pos[site]
        halfl = 0.5*sz[i]*fac
        if sz[i] > 0: c = 'b'
        else: c = 'r'
        if halfl != 0:
            #ax.arrow (x, y-halfl, dx=0, dy=2*halfl, width=0.05,length_includes_head=True,head_width=0.3,head_length=0.5*abs(halfl),fc=c,ec=c)
            plot_arrow (ax, x, y, halfl, c)

    xmin = min(zip(*pos)[0])
    ymin = min(zip(*pos)[1])
    if label:
        if '-all' in sys.argv:
            ax.text (xmin,ymin-text_shift,'$\mathrm{max } |S_z| = '+fformat(maxsz)+'$', fontsize=fontsize)
            ax.text (xmin,ymin-text_shift-1,'$\mathrm{min } |S_z| = '+fformat(minsz)+'$', fontsize=fontsize)
        elif fac > 0:
            halfl = 0.5*maxsz*fac
            #ax.text (xmin+19,ymin-text_shift-2.25,'$\langle S_i^z \\rangle$', fontsize=fontsize)
            plot_arrow (ax, xmin+21, ymin-text_shift-2, halfl, c='b')
            ax.text (xmin+23,ymin-text_shift-2.25,'$'+fformat(maxsz)+'$', fontsize=fontsize)
        else:
            print 'max sz =',max(abssz)

def plot_root3 (ax,lx,ly,xpbc,ypbc):
    links, units, N = get_kagome (lx,ly,xpbc,ypbc)

    dx,dy = 1,3**0.5
    pos = [float('Nan') for i in xrange(N)]
    lines = []
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)
            position_diamond (pos, units[i], x, y, dx=dx,dy=dy)

            if x % 3 == 0:
                c1,c2,c3 = 'r','g','b'
            elif x % 3 == 1:
                c1,c2,c3 = 'b','r','g'
            elif x % 3 == 2:
                c1,c2,c3 = 'g','b','r'
            c1pos = [pos[units[i]['up']]]
            if y != 1: c1pos.append (pos[units[i]['down']])
            c2pos = [pos[units[i]['left_up']],pos[units[i]['left_down']]]
            if x != lx: c2pos.append (pos[units[i]['right']])
            c3pos = [pos[units[i]['left']],pos[units[i]['right_up']],pos[units[i]['right_down']]]
            ax.plot (*zip(*c1pos),marker='o',c=c1,ls='None',ms=10)
            ax.plot (*zip(*c2pos),marker='o',c=c2,ls='None',ms=10)
            ax.plot (*zip(*c3pos),marker='o',c=c3,ls='None',ms=10)

def plot_kagome_bondE (ax, dat, links, pos, swp, dy=3**0.5, lw_min=1, lw_max=14, zero_en=1e-5, text_shift=3, fontsize=40, MAXen=0.5, label=True):
    ss = []
    for i,j in links:
        i = i+1
        j = j+1
        ssxy = dat[swp,'SSxy',i,j]
        ssz = dat[swp,'SSz',i,j]
        ss.append (ssxy+ssz)

    absSS = [abs(i) for i in ss]
    max_en,min_en = max(absSS),min(absSS)
    if max_en > MAXen:
        MAXen = max_en
        #print 'MAXen is too small'
        #raise Exception
    fac = lw_max/MAXen
    fac = max(0,fac)
    for link,en in zip(links,ss):
        i,j = link
        x1,y1 = pos[i]
        x2,y2 = pos[j]
        if abs(y1-y2) > 2*dy:
            if y1 > y2: y1 = y2-dy
            else: y2 = y1-dy
        if en <= 0: ls = '-'
        else: ls = '--'
        ax.plot ([x1,x2],[y1,y2],c='k',ls=ls,lw=abs(fac*en))

    xmin = min(zip(*pos)[0])
    ymin = min(zip(*pos)[1])

    if label:
        #ax.text (xmin,ymin-text_shift-2,'$\mathrm{max } |\mathrm{bond} E| = '+fformat(max_en)+'$', fontsize=18)
        #ax.text (xmin,ymin-text_shift-3,'$\mathrm{min } |\mathrm{bond} E| = '+fformat(min_en)+'$', fontsize=18)
        enlarge,ensmall = -0.4, -0.001
        ax.plot ([xmin+1,xmin+3],[ymin-text_shift-2]*2,c='k',lw=abs(fac*enlarge))
        ax.text (xmin+4,ymin-text_shift-2.25,'$'+fformat(enlarge)+'$', fontsize=fontsize)
        ax.plot ([xmin+9,xmin+11],[ymin-text_shift-2]*2,c='k',lw=abs(fac*ensmall))
        ax.text (xmin+12,ymin-text_shift-2.25,'$'+fformat(ensmall)+'$', fontsize=fontsize)

def get_local_Jz (fname):
    xJz = dict()
    with open(fname) as f:
        for line in f:
            if 'Local Jz' in line: break
        for line in f: break
        for line in f:
            tmp = line.split()
            if len(tmp) != 7: break
            i,j,x1,y1,x2,y2 = map(int,tmp[:-1])
            Jz = float(tmp[-1])
            if y1 == 1:
                if y1 < y2:
                    x = x1
                else:
                    x = x2
                xJz[x] = Jz
    return xJz

def label_local_Jz (ax,xJz,y,fontsize=16,xsh=3):
    xmin = min(xJz.keys())
    ax.text (xmin-1,y,'Jz', fontsize=fontsize, horizontalalignment='center',verticalalignment='center')
    for x in xJz:
        Jz = xJz[x]
        ax.text (x+xsh,y,Jz, fontsize=fontsize, horizontalalignment='center',verticalalignment='center')

if __name__ == '__main__':

    rc('font', **{'family': 'DejaVu Sans', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

    fontsize = 40
    text_shift = 3
    leftspace = 0
    bottomspace = 6
    label = 1
    if not label: bottomspace = 2
    if '-localjz' in sys.argv:
        text_shift += 2
        leftspace += 2

    if '-auto' in sys.argv:
        fname = glob.glob("*.out")[0]
    else:
        fname = sys.argv[1]
    with open(fname) as f:
        for line in f:
            if 'Lx =' in line: lx = int(line.split()[-1])
            if 'Ly =' in line: ly = int(line.split()[-1])
            if 'periodic_x =' in line: xpbc = int(line.split()[-1])
            if 'periodic_y =' in line: ypbc = int(line.split()[-1])
            if ' Jz =' in line: Jz = float(line.split()[-1])
    plot_kagome_lattice = plot_kagome_latticeXC
    dx,dy = 1,3**0.5
    if '-YC' in sys.argv or '-yc' in sys.argv:
        plot_kagome_lattice = plot_kagome_latticeYC
        dx,dy = 3**0.5,1

    sweeps, cutoffs, ms, terr, E, Eps = te.trunerr2 (fname,verbose=False)
    print sweeps
    datSS = get_SS (fname)
    pfiles = ''
    if '-localjz' in sys.argv:
        xJz = get_local_Jz (fname)
    with open(fname) as f:
        if '-all' not in sys.argv:
            for i in xrange(1,len(sweeps)):
                if sweeps[i-1] > sweeps[i]:
                    f = ut.file_goto (f,'Sweep='+str(sweeps[i-1]))
            sweeps = [sweeps[-1]]
            ms = [ms[-1]]
            terr = [terr[-1]]
        for swp,m,te in zip(sweeps,ms,terr):
            print 'swp =',swp
            fig,ax = pl.subplots()
            pos, links = plot_kagome_lattice (ax,lx,ly,xpbc,ypbc,ls='None',leftspace=leftspace,bottomspace=bottomspace)
            plot_kagome_sz (ax, pos, f, swp, text_shift=text_shift,fontsize=fontsize,label=label)
            plot_kagome_bondE (ax, datSS, links, pos, swp, dy=dy, text_shift=text_shift,fontsize=fontsize,label=label)#, Jz=Jz)
            #pl.title ('$J_z='+str(Jz)+'$',fontsize=40)

            xmin = min(zip(*pos)[0])
            ymin = min(zip(*pos)[1])
            if '-all' in sys.argv:
                ax.text (xmin+12,ymin-text_shift,'$m = '+str(m)+'$', fontsize=fontsize)
                ax.text (xmin+12,ymin-text_shift-1,'$\mathrm{trunc\ err} = '+fformat(te)+'$', fontsize=fontsize)
            pl.tight_layout()

            if '-localjz' in sys.argv:
                label_local_Jz (ax,xJz,y=2)

            if '-pdf' in sys.argv:
                ptmp = fname+'_m'+str(m)+'.pdf'
                pl.savefig (ptmp)
                pfiles += ' '+ptmp
            else:
                pl.show()
        if '-pdf' in sys.argv:
            if '-all' in sys.argv:
                pfile = fname+'.sz.all.pdf '
            else:
                pfile = fname+'.sz.pdf '
            os.system ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+pfile+pfiles)
            os.system ('rm '+pfiles)
