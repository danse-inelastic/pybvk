#!/usr/bin/env python

import sys

import numpy
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
  E = numpy.arange(N_Bins)*dE
  return (filetype.strip('\x00'),version,comment.strip('\x00')),E,DOS


files = sys.argv[1:]

import Gnuplot
g = Gnuplot.Gnuplot()
gd = Gnuplot.Data

for i in files:
  D = read(filename=i)
  g.replot(gd(D[1],D[2],with='l lw 4'))

raw_input("Press <Enter> to close up shop...")
