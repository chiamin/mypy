#!/bin/bash

remote="ChiaMin.Chung@th-ws-e556.theorie.physik.uni-muenchen.de"
todir="/project/thcluster/c/ChiaMin.Chung/mypy/dmrg.itensor"
#remote="chiamic@gplogin1.ps.uci.edu"
#todir="/home/chiamic/mypy/syten"
#remote="ru32web@lxlogin8.lrz.de"
#todir="/home/hpc/uh3o1/ru32web/mypy/syten"
mySrc="./*.py"
myTar=$remote:$todir/

rsync -az --progress $mySrc $myTar
