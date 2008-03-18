#!/usr/bin/env python

import numpy
from struct import pack,unpack,calcsize

intSize = calcsize('<i')

def read(D=3,filename='qs'):
  """Takes filename, returns a tuple with information and Q as a numpy."""
  f=open(filename,'r').read()
  i = 0
  N_q,     = unpack('<i',f[i:i+intSize])             ; i += intSize
  Q        = unpack('<%id' % ( N_q*(D+1) ), f[i:] )
  Q = numpy.array(Q)
  Q.shape = (N_q,D+1)
  W = Q[:,-1].copy()
  Q = Q[:,:-1].copy()
  return Q,W

version=1
dubSize = calcsize('<d')
strSize = calcsize('<s')

def writeBVK(Q,W,filename='qs.out',comment=''):
  f=open(filename,'w')
  f.write(pack('<i',Q.shape[0]))
  res = numpy.zeros( (Q.shape[0],Q.shape[1]+1) )
  res[:,:-1] = Q.copy()
  res[:,-1] = W.copy()
  res = tuple( res.reshape(-1) )
  f.write(pack('<%id' % len(res),*res))
  return

def write(Q,filename='qs',comment=''):
  """Takes numpy Q in with shape (N_q,D) and writes to binary file."""
  f=open(filename,'w')
  f.write(pack('<64s','Q'))
  f.write(pack('<i',version))
  f.write(pack('<1024s',comment))
  f.write(pack('<i',Q.shape[1]))
  f.write(pack('<i',Q.shape[0]))
  Q = tuple( Q.reshape(-1) )
  f.write(pack('<%id' % len(Q),*Q))
  return
