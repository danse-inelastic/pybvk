#!/usr/bin/env python

# USER INPUT:
# import sys
# N_b = int(sys.argv[1])

TOL    = 1e-10 # This is out of values near 1.0
bigTOL = 1e14  # This is out of values around 1e26.
import numpy
nar = numpy.add.reduce


def test(N_b):
  import qs
  import Polarizations
  import Omega2
  import D 
#----
  qs            = reload(qs)
  Polarizations = reload(Polarizations)
  D             = reload(D)
  Omega2        = reload(Omega2)
  DM = D.D
#----
  res = True
  Q,W = qs.read()  # qs spans 0 .. 2*pi
  N_q = Q.shape[0]
  Dim   = Q.shape[1]
  Pols = Polarizations.read(N_q,N_b)
  bvkOmega2 = Omega2.read(N_q,N_b)
  DM.shape = (N_b*Dim,N_b*Dim)
  pyOmega2,pyPols = numpy.linalg.eigh(DM)
  pyOmega2.shape = (N_q,N_b,Dim)
  if nar( nar( nar( (bvkOmega2 - pyOmega2)**2 ) ) )/float(N_b*Dim) < bigTOL**2:
    pass
  else:
    res = False
#    raise "Broken eigenvalue."
  tmpP = Pols.T
  tmpPyP = pyPols.T
  for i in range(len(tmpP)):
    tmp = tmpP[i] - tmpPyP[i]
    err = nar( numpy.real( tmp*numpy.conjugate(tmp) ) )
    err /= float(N_b*Dim)
    if err < TOL**2:
      pass
    else:
      tmp = tmpP[i] + tmpPyP[i]
      err = nar( numpy.real( tmp*numpy.conjugate(tmp) ) )
      err /= float(N_b*Dim)
      if err < TOL**2:
        pass
      else:
        res = False
#        raise "Broken Eigenvectors."
  return res
