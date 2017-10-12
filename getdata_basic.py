import sys, os, shutil
sys.path.append ('/home/bluewhite/mypy')
from CMC_file import *
from Binning import *
import Statistics as st
import AnalyObs3 as ao3

PARADIR = 'para'
DATDIR = 'data'
RAWDIR = 'rawdata'
JOBLIST = 'jobs.list'
try: os.mkdir (DATDIR)
except OSError: pass
os.system('cp '+PARADIR+'/'+JOBLIST+' '+DATDIR)
os.system('cp '+RAWDIR+'/*_equi.obs '+DATDIR)

OBS = ['','_E']
OBS2 = ['Z_NA']
#os.system('cp '+RAWDIR+'/*.obs3 '+DATDIR)

def special_analysis (filename, prefix):
  if os.path.exists (filename):
    obs3 = ao3.run (filename,prefix)
    for oi in obs3:
      binone.run (oi[0], oi[1-len(oi)/divide:],NBmin=1000)
      binone.write (datfile)
    fs = open(datfile.rstrip(),'aw')
    fs.write (str([prefix]+[i[0] for i in obs3]).strip('()[]\'').replace(',','').replace('\'','')+'\n')

for job in readfile((DATDIR+'/'+JOBLIST).rstrip())[0]:
  print job
  parafile, datfile = PARADIR+'/'+job+'.para', DATDIR+'/'+job+'.dat'
  # Remove data file if existed
  if os.path.exists (datfile): os.remove (datfile)
  # Copy the parameter files to data directory as a data file
  shutil.copy (parafile, datfile)
  # Read the raw data files
  raws = []
  for obs in OBS:
    rawfile = RAWDIR+'/'+job+obs+'.obs'
    if os.path.exists (rawfile): raws.append (readfile(rawfile))
  for obs2 in OBS2:
    rawfile2 = RAWDIR+'/'+job+'_'+obs2+'.obs2'
    obsname2 = RAWDIR+'/'+job+'_'+obs2+'.obs2info'
    if os.path.exists (rawfile2) and os.path.exists (obsname2):
      raws.append (zip(*(readfile(obsname2,raw=True)+readfile(rawfile2,raw=True))))
      writefile (datfile, [OBS2+readfile(obsname2, raw=True)[0]], raw=True, app=True)
  # Do binning analysis
  divide = 1
  if len(sys.argv) != 1: divide = int(sys.argv[1])
  for raw in raws:
    for rawi in raw:
      binone = BinAnaly()
      binone.run (rawi[0], rawi[1-len(rawi)/divide:],NBmin=100)
      binone.write (datfile)
  # Obs3
  special_analysis (RAWDIR+'/'+job+'.obs3','ZN')
  special_analysis (RAWDIR+'/'+job+'_2.obs3','ZN_2')
  special_analysis (RAWDIR+'/'+job+'.obs1','bb')
  '''# Read lattice observable
  lattrawfile = RAWDIR+'/'+job+'.lattobs'
  lattraw = readfile (lattrawfile, raw=True)
  obsname, lattrawdat = lattraw[0][0], lattraw[1:]
  lattrawdat = zip(*lattrawdat)
  # Binning analysis for lattice observable
  lattdat, latterr = [], []
  for di in lattrawdat:
    #binone.run (obsname, di)
    #uncorrlattraw = binone.uncorr_data()
    lattdat.append (st.mean(di)/2.e9)
    #latterr.append (st.err(di)/2.e9)
  writefile (DATDIR+'/'+job+'_'+obsname+'.lattdat', [lattraw[0], lattdat], raw=True)'''
