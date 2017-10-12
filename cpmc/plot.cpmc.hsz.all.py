import sys, os

fname = sys.argv[1]
fs = open (fname)
f = fs.readlines()
mea_exe = '/home/chiamic/cpmc/dmrg/measure.v3/measure.exe'
outfile = fname+'.pdf'

Hmpo_file = 'H.mpo'

def main():
  psiname = get ('psi_T_file',f)
  ms = get_ms (f)
  ts = get_trunc (f)
  Sites = get('hub_sites_file',f)+'.sites'
  Lx = get('Lx',f)
  tmpfiles = ''
  for i in xrange(len(ts)):
    psifile  = psiname+'.m'+ms[i]+'.mps'
    mea_file = fname+'.m'+ms[i]+'.dat'
    os.system (mea_exe+' '+Sites+' '+psifile+' '+Lx+' > '+mea_file)
    os.system ('python ~/mypy/plot.cpmc.hsz.py '+mea_file+' '+fname+' '+ts[i]+' '+ms[i])
    tmpfiles += ' '+mea_file+'.temp.ps'
    #os.system ('rm '+mea_file)
  os.system ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+outfile+tmpfiles)
  os.system ('rm '+tmpfiles+' tmp')

def get (key, f):
  for line in f:
    if key in line:
      eles = line.split() 
      return eles[-1]

def get_ms (f):
  mode = 'pass'
  ms = []
  for line in f:
    if 'Making input group' in line:
      return ms
    if all(x in line for x in ['maxm','minm','cutoff','niter','noise']):
      mode = 'read'
      continue

    if mode == 'read':
      eles = line.split()
      ms.append (eles[0])
      mode = 'pass'
  return ms

def get_trunc (f):
  mode = 'pass'
  ts = []
  for line in f:
    #print line
    if 'Making input group' in line and '.sweeps' in line:
      mode = 'new read'
      continue
    if 'Largest truncation error' in line:
      eles = line.split()
      if mode == 'new read':
        ts.append (eles[-1])
        mode = 'read'
        continue
      elif mode == 'read':
        ts[-1] = eles[-1]
        continue
  return ts

main()
