import sys, os
sys.path.append ('/home/c705/c7051023/mypy')
from CMC_file import *

JOBN = int(sys.argv[1])
os.system ('mkdir rawdata')
os.system ('cp -r 1/para .')
names = readfile('1/para/jobs.list')[0]
obsname = readfile('1/rawdata/'+names[0]+'.obs', raw=True)[0]
print obsname
for name in names:
  dat = [obsname]
  dat3o, dat3c = [], []
  for ni in range(1,JOBN+1):
    filename = str(ni)+'/rawdata/'+name+'.obs'
    dat.extend (readfile (filename, raw=True)[1:])
    filename3 = str(ni)+'/rawdata/'+name+'.obs3'
    dat3o.extend (readfile (filename3, raw=True))
    filename3 = str(ni)+'/rawdata/'+name+'_2.obs3'
    dat3c.extend (readfile (filename3, raw=True))
  writefile ('rawdata/'+name+'.obs', dat, raw=True)
  writefile ('rawdata/'+name+'.obs3', dat3o, raw=True)
  writefile ('rawdata/'+name+'_2.obs3', dat3c, raw=True)
