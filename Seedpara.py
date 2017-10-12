from CMC_file import *
import sys, random, os

para = readfile ('base.para')
ri = 0
for i in range(len(para[0])):
  if para[0][i] == 'RandSeed': ri = i
for i in range(1,int(sys.argv[1])+1):
  os.system ('mkdir '+str(i))
  para[1][ri] = random.randint (0, sys.maxint)
  writefile (str(i)+'/base.para', para)
