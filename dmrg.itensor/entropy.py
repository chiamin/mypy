import sys
import pylab as pl

def get_entropy_tmp (fname):
    dat = dict()
    with open(fname) as f:
        for line in f:
            if 'Max_m' in line:
                m = int(line.split('=')[-1])
            if 'Entanglement entropy' in line:
                tmp = line.split()
                bi = int(tmp[4].split('=')[-1])
                s = float(tmp[-1])
                if m not in dat: dat[m] = dict()
                dat[m][bi] = s
    for m, di in dat.iteritems():
        bi = di.keys()
        Si = di.values()
        dat[m] = map(list,zip(*sorted(zip(bi,Si))))
    return dat

def get_entropy (fname):
    ms,entrops = [],[]
    with open(fname) as f:
        for line in f:
            if 'Max_m' in line:
                m = int(line.split('=')[-1])
            if 'vN Entropy' in line:
                tmp = line.split()
                s = float(tmp[-1])
                ms.append (m)
                entrops.append (s)
    return ms,entrops

if __name__ == '__main__':
    fname = sys.argv[1]

    dat = get_entropy_tmp (fname)
    ms = sorted (dat.keys())
    sites,entrops = dat[ms[-1]]
    print sites[entrops.index(max(entrops))], sites
    pl.plot (sites, entrops, marker='o')
    pl.legend(loc='best')
    pl.show()
