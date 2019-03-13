import sys, os, random

def write_localmuh_random (f,lx,ly,minmu=0,maxmu=0,minh=0,maxh=0):
    for x in xrange(1,lx+1):
        for y in xrange(1,ly+1):
            mu = rnadom.uniform (minmu, maxmu)
            h = rnadom.uniform (minh, maxh)
            print>>f, '        '+str(x)+'  '+str(y)+'  '+str(mu)+'  '+str(h)

if __name__ == '__main__':
    pfile = sys.argv[1]

    Lx = 48
    Ly = 4
    Nup = Ndn = Lx*Ly*7/8/2
    delta = 10

    with open(pfile) as f:
        print>>f, 'basic'
        print>>f, '    {'
        print>>f, '    Lx = '+str(Ly)
        print>>f, '    Ly = '+str(Ly)
        print>>f, '    N_up = '+str(Nup)
        print>>f, '    N_dn = '+str(Ndn)
        print>>f, '    U = 8'
        print>>f, '    tx = 1'
        print>>f, '    ty = 1'
        print>>f, '    tpr = 0'
        print>>f, '    mu = 0'
        print>>f, '    phase = 1.'
        print>>f, '    periodic_x = 0'
        print>>f, '    periodic_y = 1'
        print>>f, '    grand_canonical = yes'
        print>>f, '    Npar_crit = 10000'
        print>>f, '    delta_potential = dwave_all'
        print>>f
        print>>f, '    initMPS = random'
        print>>f, '    // can be AF, stripes, or random'
        print>>f
        print>>f, '    stripeMPSXX'
        print>>f, '    {'
        print>>f, '        hx         = 4'
        print>>f, '        hy         = 1 2 3 4'
        print>>f, '        mu_tmp     = -1'
        print>>f, '        h_tmp      = 0.5'
        print>>f, '    }'
        print>>f
        print>>f, '    localmuh'
        print>>f, '    {'
        print>>f, '        x    y      mu      h'

        write_localmuh_random (f, Lx, Ly, minmu=1.4, maxmu=1.6)

        print>>f, '    }'
        print>>f
        print>>f, '    write_to_file = yes'
        print>>f, '    outdir = '+os.getcwd()
        print>>f, '    out_suffix = hp_10'
        print>>f, '    out_minm = 800'
        print>>f
        print>>f, '    read = no
        print>>f, '    read_dir = /mnt/ceph/users/chiaminchung/hubbard_pairing/2_sqrt2_1'
        print>>f, '    read_sites = Hub_hp_2_sqrt2_0.07.sites'
        print>>f, '    read_psi = psi_hp_2_sqrt2_0.07.m2400.mps'
        print>>f
        print>>f, '    nsweep_tmp = 0'
        print>>f, '    nsweep_main = 2'
        print>>f, '    WriteM = 5000'
        print>>f, '    quiet = no'
        print>>f, '    sweeps'
        print>>f, '    {'
        print>>f, '        m      cutoff   niter  noise    nsweep   delta'
        print>>f, '        2      1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        4      1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        8      1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        16     1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        32     1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        64     1E-10    10     1e-8     10       '+str(delta)
        print>>f, '        128    1E-10    10     1e-9     10       '+str(delta)
        print>>f, '        200    1E-12    10     1e-10    10       '+str(delta)
        print>>f, '        300    1E-12    10     0        10       '+str(delta)
        print>>f, '        500    1E-12    10     0        10       '+str(delta)
        print>>f, '        800    1E-12    10     0        10       '+str(delta)
        print>>f, '        1400   1E-12    10     0        4        '+str(delta)
        print>>f, '        2400   1E-12    8      0        4        '+str(delta)
        print>>f, '        3000   1E-12    6      0        3        '+str(delta)
        print>>f, '        4000   1E-12    4      0        3        '+str(delta)
        print>>f, '        5000   1E-12    4      0        3        '+str(delta)
        print>>f, '        6000   1E-12    4      0        3        '+str(delta)
        print>>f, '        7000   1E-12    4      0        3        '+str(delta)
        print>>f, '        8000   1E-12    4      0        3        '+str(delta)
        print>>f, '        9000   1E-12    4      0        3        '+str(delta)
        print>>f, '       10000   1E-12    4      0        3        '+str(delta)
        print>>f, '       11000   1E-12    4      0        3        '+str(delta)
        print>>f, '       12000   1E-12    4      0        3        '+str(delta)
        print>>f, '    }'
