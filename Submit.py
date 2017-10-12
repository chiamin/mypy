import sys, os, copy, shutil
from CMC_file import *
import ENVIRONMENT as envi
import random

TIME = 24 # hours
BASEPARA = 'base.para'
HOME = envi.HOME#'/home/c705/c7051023'
EXE = HOME+'/code/entanglement/exe/worm.exe'
#EXE = '/home/bluewhite//code/20120720_n_histogram/test/test.exe'
QUEUE = ''
JOBSH = HOME+'/bin/job.sh'
PARADICT = dict(readfile(BASEPARA, raw=True))
RAWDIR = PARADICT['RAWDATA_DIR']
PARADIR = PARADICT['PARA_DIR']
BACKUPDIR = PARADICT['BACKUP_DIR']
JOBLIST = PARADIR+'/jobs.list'
SUBLATTLIST = PARADIR+'/sublatt.list'
try: os.mkdir (RAWDIR)
except OSError: pass
try: os.mkdir (PARADIR)
except OSError: pass
try: os.mkdir (BACKUPDIR)
except OSError: pass

class Joblist:
  _alljobs, _jobs = [], []
  '''def __init__ (self):
    try:
      fs = open (JOBLIST.rstrip())
      self._alljobs = [a.rstrip() for a in fs.readlines()]
    except IOError: return'''
  def add (self, item):
    if item not in self._jobs: self._jobs.append (item)
    if item not in self._alljobs: self._alljobs.append (item)
  def rm (self, item):
    if item in self._jobs: self._jobs.remove(item)
    if item in self._alljobs: self._alljobs.remove(item)
  def jobs (self): return self._jobs
  def write (self, filename): writefile(filename, [self._alljobs])
joblist = Joblist()

def makepara_fromfile (filename):
  basepara, dat = readfile(BASEPARA), readfile(filename)[0]
  pfi, ind = basepara[0].index('JOB_NAME'), basepara[0].index(dat[0])
  count = 1
  for di in dat[1:]:
    # Job name
    para = copy.deepcopy(basepara)
    jobname = para[1][pfi]+'_'+dat[0]+str(count)
    para[1][pfi], para[1][ind] = jobname, di
    count += 1
    joblist.add (jobname)
    # Write files
    writefile (PARADIR+'/'+jobname+'.para', para)
  joblist.write(JOBLIST)

def makesubpara (parafile):
  'Generate the parameter files from sub-lattice files'
  para = readfile (parafile)
  ind = para[0].index ('JOB_NAME')
  origjobname = para[1][ind]
  #print origjobname
  sublattlist = readfile (SUBLATTLIST)
  for i in range(len(sublattlist[0])-1):
    newpara = [para[0]+['SUB_LATT_1', 'SUB_LATT_2'], para[1]+[sublattlist[0][i], sublattlist[0][i+1]]]
    jobname = origjobname+'_sub_'+str(i)
    print jobname
    newpara[1][ind] = jobname
    writefile (PARADIR+'/'+jobname+'.para', newpara)
    joblist.rm (origjobname)
    joblist.add (jobname)
  joblist.write (JOBLIST)

def makepara_loop ():
  status = False
  for job in joblist.jobs():
    parafile = PARADIR+'/'+job+'.para'
    if makepara(parafile):
      print job
      joblist.rm(job)
      status = True
  return status

def makepara (BASEPARA):
  def getgen ():
    'Get the generating parameters from a parameter-file'
    basepara = readfile (BASEPARA, raw=True)
    for paraitem in basepara:
      if type(paraitem[1]) is str and ':' in paraitem[1]:
        return paraitem
    return False
  def genvalue (hint):
    'Generate values from something like 1:7:2 to [1, 3, 5]'
    def frange(start, stop, step=1):
      r = [start]
      while r[-1] < stop: r.append(r[-1]+step)
      return r
    val = map(float_or_str, hint.split (':'))
    val = frange (*val)
    return val
  def set_special_term (paraitem):
    'Handle the parameters depending on other parametres'
    paradict = dict(zip(*paraitem))
    for i in range(len(paraitem[0])):
      if type(paraitem[1][i]) is str and '$' in paraitem[1][i]:
        val = paraitem[1][i].replace('$','paradict').replace('(','[\'').replace(')','\']')
        try: paraitem[1][i] = eval(val)
        except TypeError: pass
    return paraitem

  gen = getgen()
  if gen == False: return False
  name, vals = gen[0], genvalue (gen[1])
  for val in vals:
    newpara = readfile(BASEPARA)
    pfi = newpara[0].index('JOB_NAME')
    # Define the job names
    jobname = str(newpara[1][pfi])+'_'+name+'_'+str(val)
    newpara[1][pfi] = jobname
    joblist.add (jobname)
    # Creat new parameter items
    ind = newpara[0].index(name)
    newpara[1][ind] = val
    # Set special term
    newpara = set_special_term (newpara)
    # Generate random number seeds
    for i in range(len(newpara[0])):
      if newpara[0][i] == 'RandSeed' and newpara[1][i] == 0:
        newpara[1][i] = random.randint (0, sys.maxint)
        break
    # Write parameter files
    writefile (PARADIR+'/'+jobname+'.para', newpara)
  joblist.write (JOBLIST)
  return True

def submit (qsub=False):
  #print '********', sys.argv
  jobs = []
  #print len(sys.argv)
  if len(sys.argv) != 1: jobs = joblist.jobs()[int(sys.argv[1]):int(sys.argv[2])]
  else: jobs = joblist.jobs()
  #print jobs

  def confirm ():
    print 'The following jobs will be submitted:'
    for job in jobs: print job
    return raw_input ('Are you sure to submit (totally '+str(len(jobs))+' jobs) [y/n]?  ') in set(['y','Y','yes'])
  if qsub:
    if confirm():
      for job in jobs:
        jobsh = readfile (JOBSH, raw=True)
        jobsh[-1] = ['/usr/bin/time --append -o '+RAWDIR+'/'+job+'.time '+EXE+' '+PARADIR+'/'+job+'.para']
        writefile (JOBSH, jobsh, raw=True)
        os.system ('qsub -l h_rt='+str(TIME)+':0:0 -N '+job+' '+JOBSH)
  else:
    if confirm():
      for job in jobs:
        os.system ('/usr/bin/time --append -o '+RAWDIR+'/'+job+'.time '+EXE+' '+PARADIR+'/'+job+'.para &')
