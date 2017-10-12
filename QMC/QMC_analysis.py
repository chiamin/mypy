import sys
sys.path.append ('home/chiamin/mypy')
from CMC_file import *
import pylab as pl
import Statistics as st

def equi_prof (raw, plot=True, plotn=1000):
  _sum, count, sqr, ns, mean, err = 0., 0., 0., range(1,len(raw)), [], []
  for i in ns:
    _sum += raw[i]
    sqr += raw[i]*raw[i]
    count += 1.
    _mean = _sum/count
    mean.append (_mean)
    try: err.append ((sqr/count - _mean*_mean)**0.5 / count)
    except ValueError: print (i, sqr/count, _mean*_mean)
  if plot:
    itv = int(len(ns) / int(plotn))
    if itv == 0: itv = 1
    pl.errorbar (ns[::itv], mean[::itv], err[::itv])
    pl.xlabel('samples')
    pl.ylabel('mean')
    pl.show()
  return ns, mean, err

def _merge_bin (k, dat):
    'Binning the data by length k. Return: a shorter data'
    shortdata, i = [], 0
    while (i+k <= len(dat)):
      shortdata.append (st.mean (dat[i:i+k]))
      i += k
    # The last bin, which may contain less than k data
    if i != len(dat):
      shortdata.append (st.mean (dat[i:]))
    return shortdata

def _auto_corr_time (k, var, var0):
    try: return 0.5*k*var/float(var0)
    except ZeroDivisionError: return float('Nan')

def binning_prof (raw, knum=200, NBmin=100, plot=True):
  'Do binning analysis.\
   knum: number of bin-length to be simulated. (k=bin size)\
   NBmin: minimum number of bins.\
   Return: [uncorrelate_data(NBmin)], [bin_size(knum)], [auto_correlation_time(knum)]'
  uncorr_data, ks, corrtime, err = [], [], [], []
  # Calcualte kmax and kmin, bin length is graw as n*kmin, n=1,2,...
  kmax = len(raw) / NBmin
  if kmax == 0: kmax = 1
  kmin = kmax / knum
  if kmin == 0: kmin = 1
  knum = kmax / kmin
  # Mearge the bin with length k=kmin
  basedata = _merge_bin (kmin, raw)
  # Get "_ks" and "_corrtime". "_uncorr_data" remains with the largest bin-length.
  var0 = st.var (raw)
  for q in range(1, knum+1):
    uncorr_data = _merge_bin (q, basedata)
    k, var = q*kmin, st.var (uncorr_data)
    err.append (st.err(uncorr_data))
    ks.append (k)
    corrtime.append (_auto_corr_time (k, var, var0))
  if plot:
    fig, ax1 = pl.subplots()
    ax1.plot (ks, corrtime, marker='.')
    ax1.set_xlabel ('bin size')
    ax1.set_ylabel ('auto correlation time')
    ax2 = ax1.twinx()
    ax2.plot (ks,err,marker='.',c='r')
    ax2.set_ylabel ('error bar')
    pl.show()
  return uncorr_data, ks, err, corrtime

def binning (raw, k):
  uncorr = _merge_bin (k, raw)
  return st.mean (raw), st.err (uncorr)

def binning2 (raw, k_low, k_up, k_itv=1):
  err = 0.
  for k in xrange(k_low,k_up+1,k_itv):
    uncorr = _merge_bin (k, raw)
    ei = st.err (uncorr)
    if ei > err: err = ei
  return st.mean (raw), err
