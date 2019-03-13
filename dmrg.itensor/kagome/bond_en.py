def get_SS (fname):
    f = open (fname)
    dat = dict()
    for line in f:
        if 'Sweep=' in line:
            swp = int(line.split(',')[0].split('=')[-1])
        elif 'SxiSxj+SyiSyj' in line:
            tmp = line.split()
            i,j = map(int,tmp[0].split('_')[1:])
            val = float(tmp[-1])
            dat[swp,'SSxy',i,j] = val
        elif 'SziSzj' in line:
            tmp = line.split()
            i,j = map(int,tmp[0].split('_')[1:])
            val = float(tmp[-1])
            dat[swp,'SSz',i,j] = val
    return dat

