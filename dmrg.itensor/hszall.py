import sys
sys.path.append ('/home/chiamin/Projects/mypy/dmrg.itensor/')
import hsz
import trunerr as te
import utility as ut

def takedata_from_mmin (dat, ms, mmin=0):
    # get the index for the last data in each m
    ii = []
    for i in xrange(len(ms)):
        m = ms[i]
        if m >= mmin:
            ii.append (i)
    if len(ii) == 0:
        print 'minm is too big'
        print 'ms =',ms
        print 'minm =',mmin
        raise Exception

    re = []
    for i in xrange(len(dat)):
        re.append ([dat[i][j] for j in ii])
    return re


if __name__ == '__main__':
  fnames = [i for i in sys.argv[1:] if '-' not in i]
  mmin = 64
  latt = 'ordinary'
  for arg in sys.argv:
    if '-minm' in arg: mmin = int(arg.split('=')[-1])
    if arg == '-rot': latt = 'rot45'
  print 'min m =',mmin
  gc = False
  if '-gc' in sys.argv: gc = True
  mu,n = None,None


  print fnames
  for fname in fnames:
      f = open (fname)
      f,lx = hsz.file_get (f,'Lx',int)
      f,ly = hsz.file_get (f,'Ly',int)
      f.close()
      #if len(sys.argv) > 2: mmin = int(sys.argv[2])

      #if mmin < 0: start,mode = '','all' # plot the pre-sweeps part
      #else:        start,mode = 'Start main sweeps','eachm'

      sweeps, cutoffs, ms, terr, E, Eps = te.trunerr (fname)
      sweeps, cutoffs, ms, terr, E, Eps = takedata_from_mmin ((sweeps, cutoffs, ms, terr, E, Eps), ms, mmin)
      #ms, terrs, obss = hsz.get_meas_ms_once (fname,start=start,mode=mode)

      #print sweeps
      #exit()
      psfiles = ''
      for m,ter,swp in zip(ms,terr,sweeps):
          #xs,ys,nups,ndns,ns,szs,hs = obss[i]

          #with open('den_m'+str(m)+'.dat','w') as ff:
          #    for x,y,nup,ndn in zip(xs,ys,nups,ndns):
          #      print >>ff, x,y,nup,ndn
          #print (sum(nups)+sum(ndns))/(lx*ly)

          psfile = hsz.hsz_plot_dat (fname,swp,ter,latt=latt,replace=True,gc=gc)

          psfiles += ' '+psfile

      outfile = fname+'.pdf'
      hsz.os_exe ('gs -sDEVICE=pdfwrite -dEPSCrop -dNOPAUSE -dBATCH -dSAFER -sOutputFile='+outfile+psfiles)
      hsz.os_exe ('rm '+psfiles)
