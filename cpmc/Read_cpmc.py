

def read_cpmc (ff,obs):
  dats = []
  for i in range(len(obs)): dats.append([])
  f = open (ff,'r')
  for line in f:
    for i in range(len(obs)):
      ostr = obs[i] + ' = '
      if ostr in line:
        pos = line.find (ostr) + len(ostr)
        dstr = line[pos:].rstrip('\n ')
        dat = [float(di) for di in dstr.split(' ')]
        if len(dat) == 1: dats[i].append (dat[0])
        else: dats[i].append (dat)
  return dats


