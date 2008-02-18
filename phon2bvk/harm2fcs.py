#!/usr/bin/python

import numpy
nar = numpy.add.reduce
matrix = numpy.matrix
import cPickle as cp
from user import a,c,TOL

def matEqual(M0,M1):
  return nar(nar( numpy.array(M0 - M1)**2 )) < TOL

S = cp.load(open("S.pkl",'r'))
for i in range(len(S)):
  for j in range(len(S[i])):
    for k in range(len(S[i][j])):
      if S[i][j][k]**2 < TOL**2:
        S[i][j][k] = 0.0

ID = numpy.array([[1.,0,0],[0,1.,0],[0,0,1.]])
id = 'ERROR'
for i in range(len(S)):
  if matEqual(S[i],ID):
    id = i

I = S.pop(id)  # Pop identity
S.insert(0,I)  # Put identity first.

infile = open('HARMONIC', 'r')

infile.readline()
numvecs = int(infile.readline().split()[0])

selfFCS = []
bonds = []
inds = []
vecs = []
ds   = []
for n in range(numvecs):
    bond = []
    bondvec = []
    bondmat = []
    ijkl = [ int(x) for x in infile.readline().split()[1:]]
    ijkl[0] -= 1
    ijkl[1] -= 1
    i = ijkl[0]
    j = ijkl[1]
    bond.append(i)
    bond.append(j)
    for y in [ float(x) for x in infile.readline().split()]:
        bondvec.append(y)
    crap = infile.readline()
    bondmat.append([ float(x)*c for x in infile.readline().split()])
    bondmat.append([ float(x)*c for x in infile.readline().split()])
    bondmat.append([ float(x)*c for x in infile.readline().split()])
    bondvec = numpy.array(bondvec)/a
    bond.append(bondvec)
    bondmat = numpy.array(bondmat)
    bond.append(bondmat)
    if (bondvec[0]**2 + bondvec[1]**2 + bondvec[2]**2) != 0: 
        inds.append( ijkl )
        vecs.append( bondvec )
        ds.append( bondmat )
        bonds.append(bond)
    else:
      selfFCS.append(bond)

if numvecs != len(bonds) + len(selfFCS):
  raise "Shit.  Something doesn't add up."

s = {}

for i in range(len(inds)):
  if inds[i][0] < 2 and inds[i][1] < 2:
    try:
      s[('Si-Si',int( nar( vecs[i]**2 ) + TOL ))].append(i) 
    except:
      s[('Si-Si',int( nar( vecs[i]**2 ) + TOL ))] = [i] 
  elif inds[i][0] >= 2 and inds[i][1] >= 2:
    try:
      s[('V-V',int( nar( vecs[i]**2 ) + TOL ))].append(i) 
    except:
      s[('V-V',int( nar( vecs[i]**2 ) + TOL ))] = [i] 
  else:
    try:
      s[('Si-V',int( nar( vecs[i]**2 ) + TOL ))].append(i) 
    except:
      s[('Si-V',int( nar( vecs[i]**2 ) + TOL ))] = [i] 

sortedBonds = []
for key in s.keys():
  print s.keys().index(key), " of ", len(s.keys())
  sortedBonds.append([ [( s[key][0], 0)] ])
  i = 1
  while i < len( s[key] ):
    ind = s[key][i]
    b = 0
    while b < len(sortedBonds[-1]):
      base = ds[ sortedBonds[-1][b][0][0] ]
      j = 0
      while j < len(S):  
        if matEqual(base,matrix(S[j])*matrix(ds[ind])*matrix(S[j].T)):
          sortedBonds[-1][b].append( (ind, j) )
          j = len(S)
          b = len(sortedBonds[-1])
        if j == len(S) - 1 and b == len(sortedBonds[-1]) -1:
          sortedBonds[-1].append( [ (ind,0) ] )
          b = len(sortedBonds[-1])
        j += 1
      b += 1
    i += 1

for i in range(len(s.keys())):
  if i == 0:
    print "index\ttotal\tsorted total\tsubgroups..."
  p0 =  str(i) + "\t" + str( len(s[s.keys()[i]]) )
  p1 = ""
  sum = 0
  for j in range(len(sortedBonds[i])):
    p1 +=  "\t" + str( len(sortedBonds[i][j]) )
    sum += len(sortedBonds[i][j])
  print p0 + "\t" + str(sum) + "\t" + p1
  if len(s[s.keys()[i]]) != sum:
    raise "Shit.  Something doesn't add up."

cp.dump(S,open("S.pkl",'w'))
cp.dump(sortedBonds,open("sortedBonds.pkl",'w'))
cp.dump(bonds,open("bonds.pkl",'w'))
