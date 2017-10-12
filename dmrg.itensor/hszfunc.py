import sys

def get_hsz_tofile (fname, outfile=''):
    f = open(fname)

    # if outfile != '', print to file; otherwise print to screan
    sout = sys.stdout
    if outfile != '':
        fout = open(outfile,'w')
        sys.stdout = fout

    fout = open(outfile)
    for line in f:
        if '**' in line:
            break
    for line in f:
        print line.strip('\n')
        break
    for line in f:
        if '**' in line:
            break
    for line in f:
        print line.strip('\n')

    sys.stdout = sout
