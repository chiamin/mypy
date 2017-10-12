import os
from CMC_file import *

BASE_PARA = 'base.para'
PREFIX = 'mua_'
ITER_OBS, ITER_VAL = 'BH_MU_a', [0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59]

bpara = readfile (BASE_PARA)
def set_para (para, obs, val):
  ind = para[0].index(obs)
  para[1][ind] = val
  return para
def write_para (filename, para, setw=20): writefile (filename, para, setw=setw)
#write_para ('gg', bpara)
for it in ITER_VAL:
  para = set_para (bpara, ITER_OBS, it)
  dirr = PREFIX+str(it).replace('.','')
  mkdir (dirr)
  mkdir (dirr+'/dat')
  mkdir (dirr+'/init')
  mkdir (dirr+'/backup')
  write_para (dirr+'/'+dirr+'.para', para)
