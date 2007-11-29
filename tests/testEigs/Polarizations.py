#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

def read(N_q,N_b,D=3,filename='eigvec'):
  """Takes filename, returns a tuple with information and Polarizations \n
     as a numpy."""
  f=open(filename,'r').read()
  i = 0
  Pols = unpack('<%id' % (N_q*N_b*D*N_b*D*2),f[i:])
  Pols = numpy.array(Pols)
  Pols.shape = (-1,2)
  Pols = Pols[:,0] + 1j*Pols[:,1]
  Pols.shape = (N_b*D,N_b*D)
  return Pols.T # They're written out in columns, so you need to transpose
                #   after reading them in.

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Pols,filename='Polarizations',comment=''):
  """Takes numpy Polarizations with shape (N_q,N_b*D,N_b,D) and writes \n
     to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Polarizations'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  res = numpy.zeros( Pols.shape + (2,) )
  res[:,:,:,:,0] = numpy.real(Pols)
  res[:,:,:,:,1] = numpy.imag(Pols)
  f.write(pack('<i',res.shape[3]))
  f.write(pack('<i',res.shape[2]))
  f.write(pack('<i',res.shape[0]))
  res = tuple( res.reshape( (-1) ) )
  f.write( pack('<%id' % len(res),*res) )
  return
