#!/usr/bin/env python

from struct import pack,unpack,calcsize

Ldub = calcsize('=d')
Lint = calcsize('=i')
Lstr = calcsize('=s')

def write(cell,atoms,sites,bonds,symsfile,symsdir='syms',filename="system"):
  a,s,b = fatAll(atoms,sites,bonds)
  F=open(symsdir+'/'+symsfile,'r').read()
  NS, = unpack('=i',F[:Lint])
  f = open(filename,'w')
  f.write( pack('=4i',len(a),len(s),len(bonds),NS ) )
  f.write( pack('=9d',*cell) )
  for i in a:
    f.write( pack('=64sd',*i) )
  for i in sites:
    f.write( pack('=3d2i',*(i+(0,)) ) )
  for i in bonds:
    f.write( pack('=2i3d9d',*i) )
  f.write( F[Lint:] )
  f.close()
  return

def read(filename='system'):
  F=open(filename,'r').read()
  ubound = 4*Lint
  a,s,b,sy = unpack('=4i',F[:ubound])
  print filename,"contains: 1 cell,",a,"atoms,",s,"sites,", \
        b,"bonds,",sy,"symmetries"
  lbound = ubound
  ubound += 9*Ldub
  cell = unpack('=9d',F[lbound:ubound])
  #print cell
  atoms = []
  for i in range(a):
    lbound = ubound
    ubound += 64*Lstr + Ldub
    atom,mass = unpack('=64sd',F[lbound:ubound])
    atom = atom.rstrip('\x00')
    atoms.append((atom,mass))
  #print atoms
  sites = []
  for i in range(s):
    lbound = ubound
    ubound += 3*Ldub + 2*Lint
    site = unpack('=3d2i',F[lbound:ubound])
    sites.append(site)
  #print sites
  bonds = []
  for i in range(b):
    lbound = ubound
    ubound += 2*Lint + 3*Ldub + 9*Ldub
    bond = unpack('=2i3d9d',F[lbound:ubound])
    bonds.append(bond)
  #print bonds
  symmetries = F[ubound:]  # not unpacked
  #print 'read <<symmetries>>'
  return cell,atoms,sites,bonds

def axial(R,r,t):
  RdotR = float( R[0]*R[0] + R[1]*R[1] + R[2]*R[2] )
  res = []
  for i in range(3):
    for j in range(3):
      res.append( R[i]*R[j]/RdotR * ( r - t ) )
      if i==j:
        res[-1] += t
  return R[0],R[1],R[2],\
         res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8]

def modAxial(R,K,Cb):
  RdotR = float( R[0]*R[0] + R[1]*R[1] + R[2]*R[2] )
  res = []
  for i in range(3):
    for j in range(3):
      res.append( R[i]*R[j]/RdotR * K )
      if i==j:
        res[-1] += Cb[i]
  return R[0],R[1],R[2],\
         res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8]

def flattenAndTuple(x):
  for i in range(len(x)):
    x[i] = tuple( flatten(x[i]) )
  return x

def fatAll(atoms,sites,bonds):
  a = flattenAndTuple(atoms)
  s = flattenAndTuple(sites)
  b = flattenAndTuple(bonds)
  return a,s,b

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
