#!/usr/bin/env python

from struct import pack
import cPickle as cp
from numpy import array

# Symmetry preprocessing
S = cp.load(open("S.pkl",'r'))
S = array(S)
numS = len(S)

# ---
f = open("syms",'w')

# numbers
f.write(pack('=i', numS)) # number of symmetries

# Symmetries
for i in range(len(S)):
  for j in range(len(S[i])):
    for k in range(len(S[i][j])):
      f.write( pack('=d',float(S[i][j][k])) )

# --- 
f.close()
