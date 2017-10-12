import sys
sys.path.append ('/home/chiamin/Projects/mypy/dmrg')
import denprof_func as dp
import grace


if __name__ == '__main__':
  fname = sys.argv[1]
  x,h = dp.hx (fname)

  pl = grace.new()
  pl.plot (x,h)
  pl.setp (xlabel='x', ylabel='Hole density')
  grace.show()

