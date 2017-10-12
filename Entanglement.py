import scipy as sc
import numpy as np

def eigen2 (R1, R2):
  lmd1 = 0.5*(R1+(2*R2-R1**2)**0.5)
  lmd2 = R1 - lmd1
  return lmd1, lmd2

def matE (Rs):
  E = np.zeros ((len(Rs), len(Rs)))
  for i in range(len(Rs)):
    for j in range(len(Rs)):
      if i == j: E[i,j] = Rs[0]
      elif i > j: E[i,j] = Rs [i-j]
      elif abs(i-j) == 1: E[i,j] = j
  return E

def pfactor (E):
  r = [1.]
  for n in range(1,len(E)+1):
    detEn = np.linalg.det (E[:n,:n])
    r.append ((-1)**n * detEn / float(sc.factorial(n,exact=True)))
  return r

def Rn (n, lamb): return sum([a**n for a in lamb])

def extract_eigval (Rs):
  # Normalize Rs[]
  Rs = list(Rs)
  C = Rs[0]
  #for j in range(len(Rs)): Rs[j] /= C**(j+1)
  # Calculate
  E = matE (Rs)
  pfact = pfactor(E)
  #print 'factors = ',pfact
  return sc.roots(pfact)#*C

def polyfun (Rs):
  # Normalize Rs[]
  Rs = list(Rs)
  C = Rs[0]
  #for j in range(len(Rs)): Rs[j] /= C**(j+1)
  # Calculate
  E = matE (Rs)
  pfact = pfactor(E)
  return np.poly1d(pfact)
