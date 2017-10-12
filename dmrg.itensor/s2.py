import sys
sys.path.append ('/home/chiamin/Projects/mypy/dmrg.itensor')
import trunerr as te


if __name__ == '__main__':
    fname = sys.argv[1]
    sweeps, cutoffs, ms, terr, E, Eps = te.trunerr (fname)

    alphas,s2 = [],[]
    f = open (fname)
    for line in f:
        if 'Sweep=' in line: break
    for line in f:
        if 'Current alpha' in line:
            alphas.append (float(line.split()[-1]))
        if 'S2 =' in line:
            s2.append (float(line.split()[-1]))

    alpha = te.get_val (fname,'alpha_S2')
    alphas = [alpha]*(len(ms)-len(alphas)) + alphas

    print 'sweeps, cutoffs, ms, terr, E, Eps, alphas, s2'
    for i in zip(*[sweeps, cutoffs, ms, terr, E, Eps, alphas, s2]): print i
