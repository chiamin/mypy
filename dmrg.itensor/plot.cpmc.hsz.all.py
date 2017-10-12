import sys, os
import trunerr as te

fname = sys.argv[1]
fs = open (fname)
f = fs.readlines()
mea_exe = 'measure/measure.exe'
plot_py = '/home/chiamin/Projects/mypy/dmrg.itensor/plot.cpmc.hsz.py'
outfile = fname+'.pdf'

Hmpo_file = 'H.mpo'

def os_exe (command):
  print command
  os.system(command)

def main():
  psiname = get ('psi_file',f)
  sweep, cutoff, ms, ts, E, Eps = te.trunerr2(fname,0)
  print ms
  #ms = get_ms (f)
  #ts = get_trunc (f)
  Sites = get('hub_sites_file',f)+'.sites'
  Lx = get('Lx',f)
  tmpfiles = ''
  for i in xrange(len(ts)):
    psifile  = psiname+'.m'+str(ms[i])+'.mps'
    mea_file = fname+'.m'+str(ms[i])+'.dat'
    print mea_exe+' '+Sites+' '+psifile+' '+Lx+' > '+mea_file


    os_exe (mea_exe+' '+Sites+' '+psifile+' '+Lx+' > '+mea_file)
    os_exe ('python '+plot_py+' '+mea_file+' '+fname+' '+str(ts[i])+' '+str(ms[i]))


    tmpfiles += ' '+mea_file+'.temp.ps'
    os_exe ('rm '+mea_file)
  os_exe ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+outfile+tmpfiles)
  os_exe ('rm '+tmpfiles+' tmp')

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
