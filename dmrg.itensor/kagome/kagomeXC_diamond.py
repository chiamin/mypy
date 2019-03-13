import itertools
import pylab as pl

def xytoi (x,y,lx,ly):
# start from 0
    x -= 1
    y -= 1
    return x*ly + y

def get_xy_table (lx,ly):
    xy_to_i = dict()
    i_to_xy = [[] for i in xrange(lx*ly*6+ly+1)]
    label = 1
    for x in xrange(1,lx+2):
        for y in xrange(1,ly+1):
            xsh,ysh = (x-1)*4, (y-1)*4
            if x == lx+1:
                xis = [1]
                yis = [3]
            else:
                xis = [1,2,2,3,4,4]
                yis = [3,4,2,1,2,4]
            for xi,yi in zip(xis,yis):
                xx = xi+xsh
                yy = yi+ysh
                i_to_xy[label] = [xx,yy]
                xy_to_i[xx,yy] = label
                label += 1
    return i_to_xy, xy_to_i

def label_unit_diamond (unit,label):
    order = ['left','left_up','left_down','down','right_down','right_up']
    for site in order:
        unit[site] = label
        label += 1
    return unit,label

def links_in_unit (unit):
    links = []
    links.append (sorted([unit['left'],unit['left_up']]))
    links.append (sorted([unit['left'],unit['left_down']]))
    links.append (sorted([unit['left_down'],unit['right_down']]))
    links.append (sorted([unit['left_down'],unit['down']]))
    links.append (sorted([unit['right_down'],unit['down']]))
    links.append (sorted([unit['right_down'],unit['right']]))
    links.append (sorted([unit['right_up'],unit['right']]))
    links.append (sorted([unit['left_up'],unit['right_up']]))
    links.append (sorted([unit['left_up'],unit['up']]))
    links.append (sorted([unit['right_up'],unit['up']]))
    return links

def link_to_right (unitL, unitR):
    links = []
    links.append (sorted([unitL['right_down'],unitR['left_down']]))
    links.append (sorted([unitL['right_up'],unitR['left_up']]))
    return links

def plot_kagome (lx,ly,xpbc,ypbc):
    # plot
    dx,dy = 1,3**0.5
    pos = [float('Nan') for i in xrange(label)]
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

    f = pl.figure()
    xpos,ypos = zip(*pos)
    pl.plot (xpos,ypos,'ok')
    for xline,yline in lines:
        pl.plot (xline,yline,'k-')
    pl.xlim (min(xpos)-dx,max(xpos)+dx)
    xlim,ylim = pl.xlim(),pl.ylim()
    fsize = [xlim[1]-xlim[0], ylim[1]-ylim[0]]
    fsize = [0.5*i for i in fsize]
    f.set_size_inches (fsize[0], fsize[1], forward=True)

def get_kagome (lx,ly,xpbc,ypbc):
    N = lx*ly
    units = [dict() for i in xrange(N)]

    # label sites
    label = 0
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)

            xl,xr,yd,yu = x-1,x+1,y-1,y+1
            if xpbc:
                if x == 1:  xl = lx
                if x == lx: xr = 1
            if ypbc:
                if y == 1:  yd = ly
                if y == ly: yu = 1

            # label within unit
            units[i],label = label_unit_diamond (units[i],label)

            # label neighbors
            if xl > 0:   # left
                j = xytoi (xl,y,lx,ly)
                if 'left' in units[i]: units[j]['right'] = units[i]['left']
            if yd > 0:   # down
                j = xytoi (x,yd,lx,ly)
                if 'down' in units[i]: units[j]['up'] = units[i]['down']
    # label right additional sites
    for y in xrange(1,ly+1):
        i = xytoi (lx,y,lx,ly)
        units[i]['right'] = label
        label += 1
    Nsites = label

    # link
    links = []
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            i = xytoi (x,y,lx,ly)

            xl,xr,yd,yu = x-1,x+1,y-1,y+1
            if xpbc:
                if x == 1:  xl = lx
                if x == lx: xr = 1
            if ypbc:
                if y == 1:  yd = ly
                if y == ly: yu = 1

            links += links_in_unit (units[i])

            # links between units
            if xr <= lx:
                j = xytoi (xr,y,lx,ly)
                links += link_to_right (units[i], units[j])
    # remove the duplicate links
    links.sort()
    links = list(links for links,_ in itertools.groupby(links))

    return links, units, Nsites

if __name__ == '__main__':
    lx,ly = 3,2
    xpbc,ypbc = 0,1

    links, units, Nsites = get_kagome (lx,ly,xpbc,ypbc)

    print len(links)
    for i in links: print i[0],i[1]
