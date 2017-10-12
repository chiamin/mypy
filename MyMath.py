import math

def entropy (Zs):
  R = Zs[1]/float(Zs[0])
  for i in range(2,len(Zs)-1,2):
    R *= Zs[i+1] / float(Zs[i])
  try: return -math.log(R)
  except ValueError:
    print R
    for zi in Zs: print zi,
    exit()

def multiply (Zs):
  R = 1.
  for i in range(len(Zs)):
    if i % 2 == 0: R /= float(Zs[i])
    else: R *= float(Zs[i])
  return R
