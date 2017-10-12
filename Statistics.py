import math
import random as rand
import numpy as np

def msum(iterable):
    "Full precision summation using multiple floats for intermediate values"
    # Rounded x+y stored in hi with the round-off stored in lo.  Together
    # hi+lo are exactly equal to x+y.  The inner loop applies hi/lo summation
    # to each partial so that the list of partial sums remains exact.
    # Depends on IEEE-754 arithmetic guarantees.  See proof of correctness at:
    # www-2.cs.cmu.edu/afs/cs/project/quake/public/papers/robust-arithmetic.ps

    partials = []               # sorted, non-overlapping partial sums
    for x in iterable:
        i = 0
        for y in partials:
            if abs(x) < abs(y):
                x, y = y, x
            hi = x + y
            lo = y - (hi - x)
            if lo:
                partials[i] = lo
                i += 1
            x = hi
        partials[i:] = [x]
    return sum(partials, 0.0)

def mean (dat, err=False):
  mean_val = msum(dat) / float(len(dat))
  if err:
    sqr = [di*di for di in dat]
    avg, sqravg = msum(dat)/float(len(dat)), msum(sqr)/float(len(sqr))
    varr = float (sqravg - avg*avg)
    if abs(varr) < 1e-16: err_val = 0.
    else: err_val = math.sqrt (varr / float(len(dat)-1))
    return mean_val, err_val
  else:
    return mean_val

def var (dat):
  'Variance'
  sqr = [di*di for di in dat]
  avg, sqravg = mean(dat), mean(sqr)
  varr = float(sqravg - avg*avg)
  if abs(varr) < 1e-16: return 0
  else: return varr
def err (dat): return math.sqrt(var(dat) / float(len(dat)-1))
def corr (a, b):
  ab = [ai * bi for ai, bi in zip(a, b)]
  abm, am, bm, avar, bvar = mean (ab), mean(a), mean(b), var(a), var(b)
  n = float(len(a))
  return (abm - am*bm) / float(math.sqrt(avar) * math.sqrt(bvar))

def remove_outliers(data, m = 2.):
    data = np.array (data)
    d = np.abs(data - np.median(data))
    #mdev = np.median(d)
    #s = d/mdev if mdev else 0.
    return data[d<m]

def Bootstrap_resample (x_array, Nboot=500):
  xboot = []
  for i in range(Nboot):
    x = 0
    for i in range(len(x_array)): x += rand.choice (x_array)
    xboot.append (x/len(x_array))
  if Nboot==1: return xboot[0]
  else: return xboot

def Jackknife_resample (x_array):
  s = msum(x_array)
  m = float(len(x_array)-1);
  return [(s-i)/m for i in x_array]

def berr (fs): return (len(fs)*var(fs)/float(len(fs)-1))**0.5
def jerr (fs): return ((len(fs)-1)*var(fs))**0.5

def Jackknife2 (fs):
  # Jackknif analysis
  U0 = mean(fs)
  # Calculate without ith value
  M, m = float(len(fs)), float(len(fs)-1)
  def sum_except (v, i):
    sumv = 0.
    for j in range(len(v)):
      if i != j: sumv += v[j]
    return sumv
  Ui = [sum_except(fs, i)/m for i in range(len(fs))]
  # Expectation value and statistical error
  U = U0 - m*(mean(Ui) - U0)
  err = math.sqrt(m * var(Ui))
  return U, err

def Jackknife (f, argss):
  argss = zip(*argss)
  fs = [f(args) for args in argss]
  return Jackknife2 (fs)

def binning (dat, block_size=1, unfilled_bin=False):
  'Binning the data with specific block size. If <unfilled_bin>==True, the last element in the returned list could be a bin less than <block_size>.'
  # Input: 1. <dat>: an array of data.
  #        2. <block_size>: size of a single bin.
  # Output: <bin_data>: an shorter array of data after binning
  bin_data, i = [], 0
  while (i+k <= len(dat)):
    bin_data.append (mean (dat[i:i+k]))
    i += k
  if unfilled_bin == True:
    if i != len(dat):
      bin_data.append (mean (dat[i:len(dat)]))
  return bin_data

def mean_track (dat, size_lim=100):
  'Return mean value for increasing data points. Total returned numbers is less than <size_lim>.'
  # Input: 1. <dat>: an array of data.
  #        2. <size_lim>: roughly the number of returned mean data. (<= <size_lim>)
  # Output: 1. <block_dat>: an array, recording the number of data taken into mean for each returned data in <mean_dat>. To be used as the x-axis.
  #         2. <mean_dat>: an array of mean data. To be used as the y-axis.
  #         3. <err_dat>: errorbar for each mean data. To be used as the errorbars.
  def errorbar (mean, mean2):
    varr = float(mean2 - mean*mean)
    if i == 1: err = float('Nan')
    elif abs(varr) < 1e-16: err = 0
    else: err = sqrt(varr / float(i-1))
    return err
  block = len(dat) / size_lim + 1
  block_dat, mean_dat, err_dat, summ, i = [], [], [], 0., 0
  dat2, sum2 = [di*di for di in dat], 0. # for calculating errorbar
  while (i+block <= len(dat)):
    summ += msum (dat[i:i+block])
    sum2 += msum (dat2[i:i+block]) # for errorbar
    i += block
    mean = summ / float(i)
    # for errorbar --
    mean2 = sum2 / float(i)
    err = errorbar (mean, mean2)
    # -- end of calculating errorbar
    block_dat.append (i)
    mean_dat.append (mean)
    err_dat.append (err)
  # Unfilled bin:
  unfilled_num = len(dat) % block
  if unfilled_num != 0:
    summ += st.msum (dat[-unfilled_num:])
    sum2 += st.msum (dat2[-unfilled_num:])
    mean = summ / float(len(dat))
    mean2 = sum2 / float(len(dat))
    err = errorbar (mean, mean2)
    # append data
    block_dat.append (len(dat))
    mean_dat.append (mean)
    err_dat.append (err)
  return block_dat, mean_dat, err_dat

class uvar:
  _raw = []
  def __init__ (self, raw): self._raw = map(float, raw)
  def __div__ (self, other):
    a, b, avar, bvar, abcorr = mean(self._raw), mean(other._raw), var(self._raw), var(other._raw), corr(self._raw, other._raw)
    mymean, tempa, tempb = a/b, avar/a, bvar/b
    myvar = mymean * (tempa*tempa + tempb*tempb - 2.*avar*bvar*abcorr/(a*b))
    myerr = math.sqrt(myvar) / len(self._raw)
    return mymean, myerr, myvar
  def __mul__ (self, other):
    a, b, avar, bvar, abcorr = mean(self._raw), mean(other._raw), var(self._raw), var(other._raw), corr(self._raw, other._raw)
    mymean = a*b
    myvar = b*b*avar + a*a*bvar + 2.*avar*bvar*abcorr
    myerr = math.sqrt(myvar) / len(self._raw)
    return mymean, myerr, myvar

class uval:
  _mean, _var = 0., 0.
  def __init__ (self, mean, var): _mean, _var = mean, var
  def __mul__ (self, other):
    mean = self._mean*other._mean
    var = self._mean*self*_mean*other._var + other._mean*other_mean*self._var
    return uval (mean, var)
