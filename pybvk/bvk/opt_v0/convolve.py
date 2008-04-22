#!/usr/bin/env python

# Takes however many DOS in c-binary format and 1 instrument resolution file 
# and convolves each DOS with the resolution function. Output to *.conv
# --- For NRIXS --- Resolution function is _not_ a function of incident energy. 

import sys

import numpy
nar = numpy.add.reduce

from struct import pack,unpack,calcsize
intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')
version=1

def read(filename='DOS'):
  """Takes filename, returns a tuple with information and DOS as a numpy."""
  f=open(filename,'r').read()
  i = 0
  filetype, = unpack('<64s',f[i:i+64*strSize])          ; i += 64*strSize
  version,  = unpack('<i',f[i:i+intSize])               ; i += intSize
  comment,  = unpack('<1024s',f[i:i+1024*strSize])      ; i += 1024*strSize
  N_Bins,   = unpack('<i',f[i:i+intSize])               ; i += intSize
  dE,       = unpack('<d',f[i:i+dubSize])               ; i += dubSize
  DOS       = unpack('<%id' % (N_Bins),f[i:])
  DOS = numpy.array(DOS)
  E = numpy.arange(0,N_Bins*dE,dE)
  return (filetype.strip('\x00'),version,comment.strip('\x00')),E,DOS


dosFiles = sys.argv[1:-1]
resFile  = sys.argv[-1]

D = []

for i in dosFiles:
  D.append( read(filename=i) )

import io
Res = io.load(resFile)

def conv(D,Res):
  E = Res[0]
  R = Res[1]
  d = numpy.zeros(E.shape)
  ind = numpy.argmin( E**2 )
  d[ ind:ind+len(D[2]) ] = D[2]
  res = numpy.convolve(R,d,'same')
  res = res[ind:]
  E = E[ind:]
  res /= nar(res)*( E[1] - E[0] )
  return E,res


R = []
for d in range(len(D)):
  er,rr = conv(D[d],Res)
  R.append( (er,rr) )
  io.write( er, rr, numpy.zeros(rr.shape), dosFiles[d]+".conv" )

