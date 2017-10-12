import sys
sys.path.append ('/home/chiamin/mypy')
sys.path.append ('/home/chiamin/mypy/dmrg')
from CMC_file import *
import utility as ut
import fitfun as ff
import copy as cp
import pylab as pl

def sort (list1,list2):
  return [list(x) for x in zip(*sorted(zip(list1, list2), key=lambda pair: pair[0]))]

# <dat> should be a list of [[x1,y1,x2,y2,delta],...]
# dirr can be 'up' or 'right'
def get_delta_xline (y,dat,dirr='up'):
  x = []
  delta = []

  #f = readprint ('deltaprof.pl '+fname,skipline=2)
  #print f

  for line in dat:
      x1,y1,x2,y2 = int(line[0]),int(line[1]),int(line[2]),int(line[3])
      if dirr == 'up':
        if y1 != y2:
          if y1 < y2:
            ydn = y1
            yup = y2
          else:
            ydn = y2
            yup = y1
          if ydn == y:
            if x1 in x:
                ind = x.index(x1)
                delta[ind] = float(line[4])
            else:
                x.append (x1)
                delta.append (float(line[4]))
      elif dirr == 'right':
        if y1 == y2:
          if x1 < x2:
            xl = x1
            xr = x2
          else:
            xl = x2
            xr = x1
          if y1 == y:
            if xl in x:
                ind = x.index(xl)
                delta[ind] = float(line[4])
            else:
                x.append (xl)
                delta.append (float(line[4]))
  x,delta = sort (x,delta)
  return x,delta

def get_xline (y,dat,dirr,inds):
  if type(inds)==int: inds = [inds]
  re = []
  for i in range(len(inds)+1): re.append([])

  #f = readprint ('deltaprof.pl '+fname,skipline=2)
  #print f

  for line in dat:
      x1,y1,x2,y2 = int(line[0]),int(line[1]),int(line[2]),int(line[3])
      if dirr == 'up':
        if y1 != y2:
          if y1 < y2:
            ydn = y1
            yup = y2
          else:
            ydn = y2
            yup = y1
          if ydn == y:
            re[0].append (x1)
            j = 1
            for i in inds:
              re[j].append (float(line[i]))
              j += 1
      elif dirr == 'right':
        if y1 == y2:
          if x1 < x2:
            xl = x1
            xr = x2
          else:
            xl = x2
            xr = x1
          if y1 == y:
            re[0].append (xl)
            j = 1
            for i in inds:
              re[j].append (float(line[i]))
              j += 1
  x = cp.deepcopy(re[0])
  for i in range(1,len(re)):
    re[0],re[i] = sort (x,re[i])
  return re


# Get delta for every sweeps
# Return dictionary del_dict[x1,y1,x2,y2] = [sweeps, delta], where <sweep> and <delta> are lists
def get_delta_sweeps (fname, sweeps=0):
  dat = readprint ('deltaprof.pl -all '+fname, skipline=2)
  del_dict = dict() # should = [sweep, delta] for key=(x1,y1,x2,y2), where x1 <= x2
  for di in dat:
    sw,x1,y1,x2,y2,delta = int(di[0]),int(di[1]),int(di[2]),int(di[3]),int(di[4]),float(di[5])
    if x1 > x2:
      x1, x2 = x2, x1
    elif x1 == x2 and y1 > y2:
      y1, y2 = y2, y1
    key = (x1,y1,x2,y2)
    if sweeps == 0 or sw in sweeps:
      if key in del_dict:
        del_dict[key][0].append (sw)
        del_dict[key][1].append (delta)
      else:
        del_dict[key] = [[sw],[delta]]

  # sort
  for key, value in del_dict.iteritems():
    sweep = sorted(value[0])
    delta = [x for (y,x) in sorted(zip(value[0],value[1]), key=lambda pair: pair[0])]
    del_dict[key] = [sweep,delta]

  return del_dict

# Get delta for every sweeps
# Return dictionary del_dict[sweep] = [[x1,y1,x2,y2,delta],...], where x1 <= x2
def get_delta_sweeps2 (fname):
  dat = readprint ('deltaprof.pl -all '+fname, skipline=0)
  del_dict = dict()
  for di in dat[:-2]:
    sw,x1,y1,x2,y2,delta = int(di[0]),int(di[1]),int(di[2]),int(di[3]),int(di[4]),float(di[5])
    if x1 > x2:
      x1, x2 = x2, x1
    elif x1 == x2 and y1 > y2:
      y1, y2 = y2, y1
    if sw not in del_dict: 
        del_dict[sw] = [[x1,y1,x2,y2,delta]]
    else:
        del_dict[sw].append([x1,y1,x2,y2,delta])
  return del_dict


def get_delta_average (fname,sw=0,xmin=1,xmax=100000000):
    if type(fname) == str:
        del_dict = get_delta_sweeps2 (fname)
    elif type(fname) == dict:
        del_dict = fname
    if sw == 0: sw = max(del_dict.keys())
    dat = del_dict[sw]
    delta,N = 0.,0
    for x1,y1,x2,y2,di in dat:
        if x1 >= xmin and x2 >= xmin and x1 <= xmax and x2 <= xmax:
            if x1 != x2: di *= -1.
            delta += di
            N += 1
    return delta/N

def extrap_delta_average (fname,mmin=0,plot=0):
    del_dict = get_delta_sweeps2 (fname)

    terr,en,terri,ms,swps = map(list,zip(*readprint ('discwt2.p '+fname, skipline=0)))
    ms = map(int,ms)
    terri = map(float,terri)
    swps = map(int,swps)
    for ibeg in xrange(len(ms)):
        if ms[ibeg] >= mmin: break
    ibeg += 1

    terrs = terri[ibeg::2]
    deltas = []
    for i in xrange(ibeg,len(ms),2):
        swp = swps[i]
        print swp, ms[i]
        delta = get_delta_average (del_dict,swp)
        deltas.append (delta)

    fitx, fity, stddev = ff.myfit (terrs,deltas,werr=terrs,order=2)

    if plot:
        pl.plot (terrs,deltas,'ok')
        pl.plot (fitx,fity,'r-')
        pl.show()

    return fity[0], abs(deltas[-1]-fity[0]), stddev

def sort_compare (dat1, dat2, lx): # dat = [x1,y1,x2,y2,...]
    xi1,yi1,xi2,yi2 = int(dat1[0]),int(dat1[1]),int(dat1[2]),int(dat1[3])
    xj1,yj1,xj2,yj2 = int(dat2[0]),int(dat2[1]),int(dat2[2]),int(dat2[3])
    def to_ind (x,y): return x + y*lx
    i1,i2,j1,j2 = to_ind(xi1,yi1), to_ind(xi2,yi2), to_ind(xj1,yj1), to_ind(xj2,yj2)
    if i1 > i2: i1,i2 = i2,i1
    if j1 > j2: j1,j2 = j2,j1

    if i1 < j1: return -1
    elif i1 > j1: return 1
    else:
      if i2 < j2: return -1
      elif i2 > j2: return 1
      else: 0

# Extrapolate delta for all sites
def extrap_all (fname, fitpts, fitorder, refit=False):

  truns,ms,sweeps = ut.get_sweeps (fname)
  dat = get_delta_sweeps (fname, sweeps) # dat[x1,y1,x2,y2] = [sweep, delta]
  lx,ly = ut.getLxy (fname)

  def compare (dat1, dat2): return sort_compare (dat1, dat2, lx)

  re = []
  fitdat = []
  for key in dat:
    x1,y1,x2,y2 = key
    fitx = truns[-fitpts:]
    fity = dat[key][1][-fitpts:]
    fit = ff.polyfit (fitx,fity,fitorder,err=fitx)
    if refit:
      re.append ([x1,y1,x2,y2,fit[-1], truns,dat[key][1],fit])
    else:
      re.append ([x1,y1,x2,y2,fit[-1]])
  return sorted(re,cmp=compare)

# Extrapolate delta for all sites
def extrap_one (fname, fitpts, fitorder):
  truns,ms,sweeps = ut.get_sweeps (fname)
  dat = get_delta_sweeps (fname, sweeps) # dat[x1,y1,x2,y2] = [sweep, delta]
  lx,ly = ut.getLxy (fname)

  re = []
  for key in dat:
    x1,y1,x2,y2 = key
    fitx = truns[-fitpts:]
    fity = dat[key][1][-fitpts:]
    fit = ff.polyfit (fitx,fity,fitorder)
    re.append ([x1,y1,x2,y2,fit[-1]])
  return re


def plot_delta (fname,y,pl,bulkx=[],fitpts=0,fitorder=2):
  if bulkx == []:
    n = ut.getn (fname)
  else:
    n = ut.getbulkn (fname,*bulkx)
  mu = ut.getmu (fname)
  print 'mu =',mu,'  n =',n

  #---- Plot density ----
  #x,h = dp.hx (fname)
  #pl.plot (x,h,legend='density')
  #---- Plot pairing ----
  if fitpts:
    dat = extrap_all (fname, fitpts=fitpts, fitorder=fitorder)
  else:
    dat = readprint ('deltaprof.pl '+fname,skipline=2)
  x,delta = get_delta_xline (y,dat,'up')
  pl.plot (x,delta)#,legend='n='+str(round(n,3))+'(mu='+str(mu)+')')
  x,delta = get_delta_xline (y,dat,'right')
  pl.plot (x,delta,c='same')

