import sys
sys.path.append ('/home/chiamin/Projects/mypy/dmrg.itensor/')
import hsz
import trunerr as te

if __name__ == '__main__':
  fname = sys.argv[1]
  mmin = 0
  latt = 'ordinary'
  for arg in sys.argv:
    if arg == '-mmin': mmin = int(arg.split('=')[-1])
    if arg == '-rot': latt = 'rot45'

  #if len(sys.argv) > 2: mmin = int(sys.argv[2])

  if mmin < 0: start,mode = '','all' # plot the pre-sweeps part
  else:        start,mode = 'Start main sweeps','eachm'

  ms, terrs, obss = hsz.get_meas_ms_once (fname,start=start,mode=mode)

  #sweeps, cutoffs, ms, terr, E, Eps = te.trunerr2 (fname,mmin)

  psfiles = ''
  for i in xrange(len(ms)):
    if ms[i] >= mmin:
      xs,ys,nups,ndns,ns,szs,hs = obss[i]
      psfile = hsz.hsz_plot_dat (fname,xs,ys,szs,hs,suf='.m'+str(ms[i]),latt=latt)
      hsz.addlabels (psfile, terrs[i], ms[i])

      psfiles += ' '+psfile

  outfile = fname+'.pdf'
  hsz.os_exe ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+outfile+psfiles)
  hsz.os_exe ('rm '+psfiles)
