import sys,os,glob
sys.path.append ('/home/c705/c7051023/mypy')
from CMC_file import *
import Statistics as st
from shutil import copyfile

def prebin (fname,bsize=100):
  if os.path.exists (fname+'.bk'):
    print 'File','"'+fname+'.bk"','already exists. Aborted.'
    return
  dat = readfile (fname)
  bdat = [[i[0]] for i in dat]
  for i in range(len(dat[0])/bsize):
    for j in range(len(dat)):
      bdat[j].append (st.mean((dat[j][i*bsize+1:(i+1)*bsize+1])))
  copyfile (fname,fname+'.bk')
  writefile (fname,bdat)
  print 'size before:',len(dat[0]), '| size after:',len(bdat[0])

obs = glob.glob ('*.obs')
for fname in obs:
  if not 'equi' in fname:
    print fname
    prebin (fname)
