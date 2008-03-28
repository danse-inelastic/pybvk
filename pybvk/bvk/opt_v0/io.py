import numpy

def load(filename):
  fi = open(filename,'r')
  f = fi.readlines()
  fi.close()
  for i in range(len(f)):
    f[i] = f[i].split()
    for j in range(len(f[i])):
      f[i][j] = float(f[i][j])
  f = numpy.array(f)
  e = numpy.array( f[:,0] )
  d = numpy.array( f[:,1] )
  r = numpy.array( f[:,2] )
  return e,d,r

def write(e,d,r,filename):
  F = open(filename,'w')
  for i in range(len(e)):
    F.write( str( e[i] ) + " " + str( d[i] ) + " " + str( r[i] ) + "\n" )
  F.close()
  return
