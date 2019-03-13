import sys, os
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
import pylab as pl
import trunerr as te
import utility as ut
from kagomeYC import get_kagome

def xytoi (x,y,lx,ly):
    x -= 1
    y -= 1
    return x*ly + y

def position_diamond (pos,unit,x,y,dx=3**0.5,dy=1):
    xoffset = x*4*dx
    yoffset = y*4*dy
    pos[unit['left']] = [xoffset, yoffset]
    pos[unit['left_up']] = [xoffset+dx, yoffset+dy]
    pos[unit['left_down']] = [xoffset+dx, yoffset-dy]
    pos[unit['down']] = [xoffset+2*dx, yoffset-2*dy]
    pos[unit['right_down']] = [xoffset+3*dx, yoffset-dy]
    pos[unit['right_up']] = [xoffset+3*dx, yoffset+dy]
    pos[unit['up']] = [xoffset+2*dx, yoffset+2*dy]
    if 'right' in unit:
        pos[unit['right']] = [xoffset+4*dx, yoffset]

def lines_diamond (x,y,dx=1,dy=3**0.5,typ=''):
    xoffset = x*4*dx
    yoffset = y*4*dy
    # diamond
    xline = [0, 2*dx, 4*dx, 2*dx, 0]
    yline = [0, -2*dy, 0, 2*dy, 0]
    xline = [i+xoffset for i in xline]
    yline = [i+yoffset for i in yline]
    dline = [xline,yline]
    # vertical
    x0,x1 = xoffset+dx, xoffset+3*dx
    y0,y1 = yoffset-2*dy, yoffset+2*dy
    #if typ == 'left': x0 += dx
    #if typ == 'right': x1 -= dx
    line1 = [[x0,x0],[y0,y1]]
    line2 = [[x1,x1],[y0,y1]]
    return [dline,line1,line2]

def plot_kagome_lattice (ax,lx,ly,xpbc,ypbc,ls='-',bottomspace=10,leftspace=0):
    links, units, N = get_kagome (lx,ly,xpbc,ypbc)

    dx,dy = 3**0.5,1
    pos = [float('Nan') for i in xrange(N)]
    lines = []
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)
            position_diamond (pos, units[i], x, y, dx=dx,dy=dy)

            lines += lines_diamond (x,y, dx=dx,dy=dy)

    xpos,ypos = zip(*pos)
    ax.plot (xpos,ypos,'ok')
    for xline,yline in lines:
        ax.plot (xline,yline,c='k',ls=ls)
    ax.set_xlim (min(xpos)-dx-leftspace,max(xpos)+dx)
    ax.set_ylim (min(ypos)-bottomspace,max(ypos)+dy)
    xlim,ylim = ax.get_xlim(),ax.get_ylim()
    fsize = [xlim[1]-xlim[0], ylim[1]-ylim[0]]
    fsize = [0.5*i for i in fsize]
    f = pl.gcf()
    f.set_size_inches (fsize[0], fsize[1], forward=True)
    return pos, links

def plot_root3 (ax,lx,ly,xpbc,ypbc):
    links, units, N = get_kagome (lx,ly,xpbc,ypbc)

    dx,dy = 3**0.5,1
    pos = [float('Nan') for i in xrange(N)]
    lines = []
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)
            position_diamond (pos, units[i], x, y, dx=dx,dy=dy)

            if y % 3 == 0:
                c1,c2,c3 = 'r','g','b'
            elif y % 3 == 1:
                c1,c2,c3 = 'b','r','g'
            elif y % 3 == 2:
                c1,c2,c3 = 'g','b','r'
            c1pos = [pos[units[i]['left_down']],pos[units[i]['right_down']],pos[units[i]['up']]]
            c2pos = [pos[units[i]['left_up']],pos[units[i]['right_up']]]
            if y != 1: c2pos.append (pos[units[i]['down']])
            c3pos = [pos[units[i]['left']]]
            if 'right' in units[i]:
                c3pos.append (pos[units[i]['right']])
            ax.plot (*zip(*c1pos),marker='o',c=c1,ls='None',ms=10)
            ax.plot (*zip(*c2pos),marker='o',c=c2,ls='None',ms=10)
            ax.plot (*zip(*c3pos),marker='o',c=c3,ls='None',ms=10)

