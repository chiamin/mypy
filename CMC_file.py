import os
import subprocess as sp

def get_from (fname, sep_line):
  f = open (fname.rstrip(), 'r')
  re = []
  for line in f:
    if sep_line in line: break
  for line in f:
    re.append (line)
  return re

def get_key (lines, key):
  for line in lines:
    if key in line:
      pos = line.find (key) + len(key)
      dstr = line[pos:].rstrip('\n ')
      return dstr


def mkdir (dirr):
  if not os.path.exists (dirr): os.mkdir (dirr)

class mydict:
  _dict = {}
  def __init__ (self,keys):
    for x in keys: self._dict[x] = []
  def __getitem__ (self,key): return self._dict[key]
  def sappend (self,items):
    for i in self._dict: self._dict[i].append (items[i])
  def app (self,key,item):
    if key in self._dict: self._dict[key].append(item)
    else: self._dict[key] = [item]

def float_or_str (a):
  try:
    a = float(a)
    aint = int(a)
    if a == aint: a = aint
  except ValueError: pass
  return a

def readfile (fname, raw=False, skipline=0, skipback=0):
  fs = open (fname.rstrip())
  for i in xrange(skipline): next (fs)
  dat = []
  for line in fs: dat.append (list(map (float_or_str, line.split())))
  if skipback: dat = dat[:-skipback]
  if raw: return dat
  else: return list(map(list, zip(*dat)))

def writefile (fname, dat, raw=False, app=False, setw=0):
  def writeline (fs,dati):
    for i in range(len(dati)):
      datj = dati[i]
      if type(datj) is not str: datj = repr(datj)
      if setw > 0:
        if i != len(dati)-1: fs.write (('{0:<'+str(setw)+'}').format(datj))
        else: fs.write (datj)
      else:
        if i != 0: fs.write (' ')
        fs.write (datj)
    fs.write('\n')

  if app: fs = open (fname.rstrip(), 'a')
  else: fs = open (fname.rstrip(), 'w')
  if raw:
    for dati in dat: writeline (fs,dati)
      #fs.write (str(dati).strip('()[]\'').replace(',','').replace('\'','')+'\n')
  else:
    if app:
      #old = readfile (fname, raw)
      #print (old)
      #print (dat)
      #dat.extend (old)
      fs = open (fname.rstrip(), 'a')
      for dati in zip(*dat): writeline (fs,dati)
        #fs.write (str(dati).strip('()[]\'').replace(',','').replace('\'','')+'\n')
    else:
      for dati in zip(*dat): writeline (fs,dati)
        #fs.write (str(dati).strip('()[]\'').replace(',','').replace('\'','')+'\n')

def readprint (command,skipline=0,typ=None):
  # command should be a list with elements of command and arguments
  dat = sp.check_output(command.split())
  dat = dat.rstrip().split('\n')
  dat = dat[skipline:]
  if typ != None:
    dat = [map(typ,i.split()) for i in dat]
  else:
    dat = [i.split() for i in dat]
  return dat


def CMC_file_example ():
  # Write data to file
  x, y = [1,2,3], [1,2,3]
  writefile ('test.dat', (x,y))

  #Read data from file
  dat = readfile ('test.dat')
  print (dat[0], '\n', dat[1])
