import sys, os

Sites   = sys.argv[1]
psifile = sys.argv[2]
Lx      = sys.argv[3]

mea_exe = '/home/chiamin/Projects/CPMC/dmrg/measure/measure.exe'
plot_py = '/home/chiamin/Projects/mypy/dmrg.itensor/plot.cpmc.hsz.py'
mea_file = psifile+'.dat'

def os_exe (command):
  print command
  os.system(command)

os_exe (mea_exe+' '+Sites+' '+psifile+' '+Lx+' > '+mea_file)
os_exe ('python '+plot_py+' '+mea_file)
