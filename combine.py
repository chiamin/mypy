import sys, os
sys.path.append ('/home/c705/c7051023/mypy')
from CMC_file import *

OBS = ['.obs','_2.obs','_3.obs']
SUFFIX = ['.obs3','_2.obs3','_open.obs3','_close.obs3','.obs1']
JOBN = int(sys.argv[1])

def combine (name, dat=[], num=float('Inf')):
  datlen = len(dat)
  for ni in range(1,JOBN+1):
    filename = str(ni)+'/rawdata/'+name
    if os.path.exists (filename):
      di = readfile (filename, raw=True)
      if num >= len(di): dat.extend (di[1:])
      else: dat.extend (di[-num:])
  if len(dat) != datlen: writefile ('rawdata/'+name, dat, raw=True)

if os.path.exists ('rawdata'): os.system ('rm rawdata/*')
else: os.system ('mkdir rawdata')
os.system ('cp -r 1/para .')
names = readfile('1/para/jobs.list')[0]
#obsname = readfile('1/rawdata/'+names[0]+'.obs', raw=True)[0]
for name in names:
  for oi in OBS:
    ni = name+oi
    obsname = readfile('1/rawdata/'+name+oi,raw=True)[0]
    print obsname
    if len(sys.argv) == 2: combine (ni, [obsname])
    elif len(sys.argv) == 3: combine (ni,[obsname],int(sys.argv[2]))
  for si in SUFFIX: combine (name+si)
