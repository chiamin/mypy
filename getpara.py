_dict = dict()

def number_or_str (a):
  try:
    a = float(a)
    aint = int(a)
    if a == aint: a = aint
  except ValueError: pass
  return a

def read (fname):
  # Save the file information in a dictionary
  fs = open (fname.rstrip())
  for line in fs.readlines():
    ele = line.split()
    if len(ele) > 2: _dict[ele[0]] = ele[1:]
    else: _dict[ele[0]] = ele[1]

def get (key):
  try: return number_or_str(_dict[key])
  except TypeError: return map(number_or_str, _dict[key])
