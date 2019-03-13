import itertools
import pylab as pl

def xytoi (x,y,lx,ly):
    x -= 1
    y -= 1
    return x*ly + y

def label_unit_diamond (unit,label):
    order = ['left','left_down','left_up','up','right_up','right_down']
    for site in order:
        unit[site] = label
        label += 1
    return unit,label

def links_in_unit (unit):
    links = []
    links.append (sorted([unit['left'],unit['left_up']]))
    links.append (sorted([unit['left'],unit['left_down']]))
    links.append (sorted([unit['left_down'],unit['left_up']]))
    links.append (sorted([unit['left_down'],unit['down']]))
    links.append (sorted([unit['left_up'],unit['up']]))
    links.append (sorted([unit['right_up'],unit['up']]))
    links.append (sorted([unit['right_down'],unit['down']]))
    links.append (sorted([unit['right_up'],unit['right_down']]))
    if 'right' in unit:
        links.append (sorted([unit['right_up'],unit['right']]))
        links.append (sorted([unit['right_down'],unit['right']]))
    return links

def link_to_up (unitDn, unitUp):
    links = []
    links.append (sorted([unitDn['left_up'],unitUp['left_down']]))
    links.append (sorted([unitDn['right_up'],unitUp['right_down']]))
    return links

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
            if yu <= ly:   # up
                j = xytoi (x,yu,lx,ly)
                if 'up' in units[i]: units[j]['down'] = units[i]['up']
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
            if yu <= ly:
                j = xytoi (x,yu,lx,ly)
                links += link_to_up (units[i], units[j])
    # remove the duplicate links
    links.sort()
    links = list(links for links,_ in itertools.groupby(links))

    return links, units, Nsites

if __name__ == '__main__':
    lx,ly = 2,1
    xpbc,ypbc = 0,1

    links, units, Nsites = get_kagome (lx,ly,xpbc,ypbc)

    print len(links)
    for i in links: print i[0],i[1]
