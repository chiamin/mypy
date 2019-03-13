import sys, os
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import pylab as pl
import trunerr as te
import utility as ut
from kagomeXC_diamond import get_kagome
from bond_en import get_SS

def xytoi (x,y,lx,ly):
    x -= 1
    y -= 1
    return x*ly + y

def position_diamond (pos,unit,x,y,dx=1,dy=3**0.5):
    xoffset = x*4*dx
    yoffset = y*4*dy
    pos[unit['left']] = [xoffset, yoffset]
    pos[unit['left_up']] = [xoffset+dx, yoffset+dy]
    pos[unit['left_down']] = [xoffset+dx, yoffset-dy]
    pos[unit['down']] = [xoffset+2*dx, yoffset-2*dy]
    pos[unit['right_down']] = [xoffset+3*dx, yoffset-dy]
    pos[unit['right_up']] = [xoffset+3*dx, yoffset+dy]
    pos[unit['up']] = [xoffset+2*dx, yoffset+2*dy]
    pos[unit['right']] = [xoffset+4*dx, yoffset]

def lines_diamond (x,y,dx=1,dy=3**0.5,typ=''):
    xoffset = (x-1)*4*dx
    yoffset = (y-1)*4*dy
    # diamond
    xline = [0, 2*dx, 4*dx, 2*dx, 0]
    yline = [0, -2*dy, 0, 2*dy, 0]
    xline = [i+xoffset for i in xline]
    yline = [i+yoffset for i in yline]
    dline = [xline,yline]
    # horizontal
    x0,x1 = xoffset, xoffset+4*dx
    y0,y1 = yoffset-dy, yoffset+dy
    if typ == 'left': x0 += dx
    if typ == 'right': x1 -= dx
    hline1 = [[x0,x1],[y0,y0]]
    hline2 = [[x0,x1],[y1,y1]]
    return [dline,hline1,hline2]

def plot_kagome_lattice (ax,lx,ly,xpbc,ypbc,ls='-',bottomspace=10,leftspace=0):
    links, units, N = get_kagome (lx,ly,xpbc,ypbc)

    dx,dy = 1,3**0.5
    pos = [float('Nan') for i in xrange(N)]
    lines = []
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)
            position_diamond (pos, units[i], x, y, dx=dx,dy=dy)

            typ = ''
            if not xpbc:
                if x == 1: typ = 'left'
                if x == lx: typ = 'right'
            lines += lines_diamond (x,y,typ=typ, dx=dx,dy=dy)

    xpos,ypos = zip(*pos)
    ax.plot (xpos,ypos,'ok')
    for xline,yline in lines:
        ax.plot (xline,yline,c='k',ls=ls)
    ax.set_xlim (min(xpos)-dx-leftspace, max(xpos)+dx)
    ax.set_ylim (ymin=min(ypos)-bottomspace)
    xlim,ylim = ax.get_xlim(),ax.get_ylim()
    fsize = [xlim[1]-xlim[0], ylim[1]-ylim[0]]
    fsize = [0.5*i for i in fsize]
    f = pl.gcf()
    f.set_size_inches (fsize[0], fsize[1], forward=True)
    ax.axis('off')
    return pos, links

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

