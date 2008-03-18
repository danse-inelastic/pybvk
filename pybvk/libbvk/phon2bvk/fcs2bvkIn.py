#!/usr/bin/env python

import numpy
matrix = numpy.matrix
array  = numpy.array

from user import a

import cPickle as cp
S  = cp.load(open("S.pkl",'r'))
B  = cp.load(open("bonds.pkl",'r'))
sB = cp.load(open("sortedBonds.pkl",'r'))

def bond2list(bond):
  bond[2] = bond[2].tolist()
  bond[3] = bond[3].tolist()
  return 

def flatten(l, ltypes=(list, tuple)):
  i = 0
  while i < len(l):
    while isinstance(l[i], ltypes):
      if not l[i]:
        l.pop(i)
        if not len(l):
          break
      else:
        l[i:i+1] = list(l[i])
    i += 1
  return l

def listFlatten(l):
  bond2list(l)
  return flatten(l)


bases = []
for i in sB:
  for j in i:
    bases.append(j[0][0])

# Zeros out FCTs for bonds that are not in bases. -- Only for testing, I guess.
for b in range(len(B)):
  if bases.count(b) != 1:
    B[b][3] -= B[b][3]
  
# Modify an FCT here:
# B[16][3] *= 1.2 # 16 is in bases.
# Replace FCT with rotated base FCT.

for i in range(len(sB)):
  for j in range(len(sB[i])):
    for k in range(len(sB[i][j])):
      l = sB[i][j][0][0]
      b = sB[i][j][k][0]
      s = sB[i][j][k][1]
      B[ b ][3] = matrix(S[s].T)*matrix(B[l][3])*matrix(S[s])
      B[ b ][2] *= a

for b in range(len(B)):
  B[b] = listFlatten(B[b])

print B
