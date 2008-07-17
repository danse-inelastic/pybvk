#!/usr/bin/env python

import sys

import numpy

def writeDOS(files):
  "converts DOS files from libbvk.fwd to human readable files"
  from g import read
  for i in files:
    D = read(filename=i)
    C = zip(D[1],D[2])
    w = open('_'+i,'w')
    for j in range(len(D[1])):
      w.write(str(C[j][0])+" "+str(C[j][1])+" 0.0\n")
    w.close()

  return


if __name__ == '__main__':
  files = sys.argv[1:]
  writeDOS(files)
