import math
import Statistics as st

class BinAnaly:
  'Doing the binning analysis'
  _name, _uncorr_data, _ks, _corrtime = '', [], [], []
  _err = []
  def __init__ (self): self._name, self._uncorr_data, self._ks, self._corrtime = '', [], [], []
  def uncorr_data(self): return self._uncorr_data
  def auto_corr_data(self): return self._ks, self._corrtime
  def write (self, datfile):
    fs = open (datfile.rstrip(), 'aw')
    fs.write (self._name+' '+str(self._uncorr_data).strip('[]').replace(',','')+'\n')
    fs.write (self._name+'_binsize '+str(self._ks).strip('[]').replace(',','')+'\n')
    fs.write (self._name+'_corrtime '+str(self._corrtime).strip('[]').replace(',','')+'\n')

  def run (self, name, dat, knum=200, NBmin=100):
    'Do binning analysis. knum: number of bin-length to be simulated. NBmin: minimum number of bins. Return: [[uncorrelate_data(NBmin)], [bin_size(knum)], [auto_correlation_time(knum)]]'
    self._name = name
    # Calcualte kmax and kmin, bin length is graw as n*kmin, n=1,2,...
    kmax = len(dat) / NBmin
    if kmax == 0: kmax = 1
    kmin = kmax / knum
    if kmin == 0: kmin = 1
    knum = kmax / kmin
    # Mearge the bin with length k=kmin
    basedata = self._merge_bin (kmin, dat)
    # Get "_ks" and "_corrtime". "_uncorr_data" remains with the largest bin-length.
    var0 = st.var (dat)
    for q in range(1, knum+1):
      self._uncorr_data = self._merge_bin (q, basedata)
      k, var = q*kmin, st.var (self._uncorr_data)
      self._err.append ([k,st.err(self._uncorr_data)])
      self._ks.append (k)
      self._corrtime.append (self._auto_corr_time (k, var, var0))

  def _merge_bin (self, k, dat):
    'Binning the data by length k. Return: a shorter data'
    shortdata, i = [], 0
    while (i+k <= len(dat)):
      shortdata.append (sum (dat[i:i+k])/float(k))
      i += k
    return shortdata
  def _auto_corr_time (self, k, var, var0):
    try: return 0.5*k*var/float(var0)
    except ZeroDivisionError: return float('Nan')
