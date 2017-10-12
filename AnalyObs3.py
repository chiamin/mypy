from CMC_file import *
import Statistics as st

def run (filename, prefix):
  a = readfile (filename, raw=True)
  # Read keys
  keys = []
  for ai in a:
    ki = ai[:-1]#[ai[0],ai[1]]
    if ki not in keys: keys.append (ki)
  keys.sort()
  # Read data
  r = {}
  i = 0
  while i < len(a):
    for k in keys:
      key = prefix+'_'+str(k).strip('[]').replace(', ','_')#str(k[0])+'_'+str(k[1])
      if i < len(a) and k == a[i][:-1]:#k[0] == a[i][0] and k[1] == a[i][1]:
        try: r[key].append (a[i][-1])
        except KeyError: r[key] = [a[i][-1]]
        i += 1
      else:
        try: r[key].append (0)
        except KeyError: r[key] = [0]
  return [[k]+i for k, i in r.iteritems()]
  #writefile ('data/'+filename+'.dat3', tolist, raw=True)
#run ('L4W_W2_1_SUB_LX_4')
