#!/usr/bin/env python

import numpy
nar = numpy.add.reduce
import cPickle as cp

Tol = 1e-10

#-----------------------------------------------------------------------------
# Rotations about n fold axis a: C_na
#-----------------------------------------------------------------------------
from numpy import cos
from numpy import sin
from numpy import pi

a2  = 180*pi/180.0
a3  = 120*pi/180.0
a4  =  90*pi/180.0
a6  =  60*pi/180.0
a12 =  30*pi/180.0

C_2y  = numpy.matrix([[ cos(a2),      0,-sin(a2)],
                      [       0,      1,       0],
                      [ sin(a2),      0, cos(a2)]])

C_3y  = numpy.matrix([[ cos(a3),      0,-sin(a3)],
                      [       0,      1,       0],
                      [ sin(a3),      0, cos(a3)]])

C_4y  = numpy.matrix([[ cos(a4),      0,-sin(a4)],
                      [       0,      1,       0],
                      [ sin(a4),      0, cos(a4)]])

C_6y  = numpy.matrix([[ cos(a6),      0,-sin(a6)],
                      [       0,      1,       0],
                      [ sin(a6),      0, cos(a6)]])

C_2x  = numpy.matrix([[      1,       0,       0],
                      [      0, cos(a2), sin(a2)],
                      [      0,-sin(a2), cos(a2)]])

C_3x  = numpy.matrix([[      1,       0,       0],
                      [      0, cos(a3), sin(a3)],
                      [      0,-sin(a3), cos(a3)]])

C_4x  = numpy.matrix([[      1,       0,       0],
                      [      0, cos(a4), sin(a4)],
                      [      0,-sin(a4), cos(a4)]])

C_6x  = numpy.matrix([[      1,       0,       0],
                      [      0, cos(a6), sin(a6)],
                      [      0,-sin(a6), cos(a6)]])

C_2z = numpy.matrix([[ cos(a2), sin(a2),      0],
                     [-sin(a2), cos(a2),      0],
                     [       0,       0,      1]])

C_3z = numpy.matrix([[ cos(a3), sin(a3),      0],
                     [-sin(a3), cos(a3),      0],
                     [       0,       0,      1]])

C_4z  = numpy.matrix([[ cos(a4), sin(a4),      0],
                      [-sin(a4), cos(a4),      0],
                      [       0,       0,      1]])

C_6z  = numpy.matrix([[ cos(a6), sin(a6),      0],
                      [-sin(a6), cos(a6),      0],
                      [       0,       0,      1]])

C_12z  = numpy.matrix([[ cos(a12), sin(a12),      0],
                       [-sin(a12), cos(a12),      0],
                       [        0,        0,      1]])


#-----------------------------------------------------------------------------
# Reflection about plane perpendicular to given vector v: R_v
# R_xy == Reflection about plane perpendicular to vector x ==  y, z == 0
#-----------------------------------------------------------------------------

R_y  = numpy.matrix([[ 1, 0, 0],
                     [ 0,-1, 0],
                     [ 0, 0, 1]] )

R_z  = numpy.matrix([[ 1, 0, 0],
                     [ 0, 1, 0],
                     [ 0, 0,-1]] )

R_x  = numpy.matrix([[-1, 0, 0],
                     [ 0, 1, 0],
                     [ 0, 0, 1]] )

I    = numpy.matrix([[-1, 0, 0],
                     [ 0,-1, 0],
                     [ 0, 0,-1]] )


def closeSyms(S):
  currentLength = 0
  while len(S) != currentLength:
    currentLength = len(S)
    candidates = []
    for i in S:
      for j in S:
        candidates.append( i*j )
    for i in candidates:
      addit = True
      for j in S:
        if nar(nar( (numpy.array(i - j))**2 )) < Tol :
          addit = False
      if addit:
        S.append(i)
  for i in range(len(S)):
    S[i] = numpy.array(S[i])
  print len(S), " symmetries generated."
  return S


from struct import pack
import os

def writeSyms(S,filename='syms',symsdir='./syms'):
  numS = len(S)
  # ---
  os.system('mkdir -p '+symsdir)
  f = open(symsdir+'/'+filename,'w')
  # numbers
  f.write(pack('=i', numS)) # number of symmetries
  # Symmetries
  for i in range(len(S)):
    for j in range(len(S[i])):
      for k in range(len(S[i][j])):
        f.write( pack('=d',float(S[i][j][k])) )
  # --- 
  f.close()
  return
