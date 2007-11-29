#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

def read(N_q,N_b,D=3,filename='eigval'):
  """Takes filename, returns a tuple with information and Omega2 as a numpy."""
  f=open(filename,'r').read()
  i = 0
  Omega2    = unpack('<%id' % (N_q*N_b*D),f[i:])
  Omega2 = numpy.array(Omega2)
  Omega2.shape = (N_q,N_b,D)
  return Omega2

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

def write(Omega2,filename='Omega2',comment=''):
  """Takes numpy Omega2 in with shape (N_q,N_b,D) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Omega2'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',Omega2.shape[2]))
  f.write(pack('<i',Omega2.shape[1]))
  f.write(pack('<i',Omega2.shape[0]))
  Omega2 = tuple( Omega2.reshape(-1) )
  f.write(pack('<%id' % len(Omega2),*Omega2))
  return
