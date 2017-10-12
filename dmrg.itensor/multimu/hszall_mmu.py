import sys
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/')
sys.path.append ('/home/chiamin/mypy/dmrg.itensor/multimu')
import hsz
import trunerr as te
import utility_mmu as ut

if __name__ == '__main__':
  fname = sys.argv[1]
  mmin = 0
  latt = 'ordinary'
  for arg in sys.argv:
    if arg == '-mmin': mmin = int(arg.split('=')[-1])
    if arg == '-rot': latt = 'rot45'


  if mmin < 0: start,mode = '','all' # plot the pre-sweeps part
  else:        start,mode = 'Start main sweeps','eachm'

  N_states = ut.get_N_mu (fname)
  for ist in xrange(N_states):
      ms, terrs, obss = hsz.get_meas_ms_once (fname,start=start,mode=mode,subkey=' , State '+str(ist))

      psfiles = ''
      for i in xrange(len(ms)):
        if ms[i] >= mmin:
          xs,ys,nups,ndns,ns,szs,hs = obss[i]
          psfile = hsz.hsz_plot_dat (fname,xs,ys,szs,hs,suf='.m'+str(ms[i]),latt=latt)
          hsz.addlabels (psfile, terrs[i], ms[i])

          psfiles += ' '+psfile

      outfile = fname+'_state'+str(ist)+'.pdf'
      hsz.os_exe ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+outfile+psfiles)
      hsz.os_exe ('rm '+psfiles)
