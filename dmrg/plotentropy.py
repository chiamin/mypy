import sys, re, os
sys.path.append('/home/chiamin/Projects/mypy')
from CMC_file import *
import grace
from entropy_func import read_entropy

gr = grace.new()

def main ():
  if len(sys.argv) <= 1: return

  fname = sys.argv[1]
  if len(sys.argv) > 2: STEP = sys.argv[2]
  else: STEP = '10000'
  plot_entropy_grace (fname,STEP)
  #plot_entropy_all (fname,STEP)


def plot_entropy_grace (fname,STEP=10000):
  xcol, Scol = read_entropy (fname,STEP)
  gr.plot (xcol,Scol)
  gr.setp (xlabel='Site',ylabel='Entropy')
  grace.show ()

def plot_entropy_all (fname,STEP=10000):
  x,y,i,S = read_entropy (fname,STEP,ALL=True)
  gr.plot (range(len(S)),S)
  gr.setp (xlabel='index',ylabel='Entropy')
  grace.show ()

def plotetrp (fname,STEP=10000,lb='',c='1',ls='1'):
  print fname
  dat = readprint (['entropy.pl',fname,str(STEP)])
  dat = zip(*dat)
  n = len(dat[3])/2
  y = dat[3][n:]
  x = range(len(y))
  #x = [i/float(len(y)) for i in x]
  gr.plot(x,y,legend=lb,c=c,ls=ls)

def getsize (string):
  search = re.search("huben(\d+)x(\d+)",string)
  return search.group(1), search.group(2)

def plotetrp_length (files,STEP=10000):
  x,y = [],[]
  for fname in files:
    lx,ly = getsize (fname)
    x.append(lx)
    dat = readprint (['entropy.pl',fname,str(STEP)])
    entrops = zip(*dat)[3]
    mid = len(entrops)/4
    y.append(entrops[mid])
  gr.plot(x,y)

main()
