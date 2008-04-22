#!/usr/bin/env python

# Take a dictionary with fcsnames and fcs, produce a System file.
def toSys(Pdict,fileIn,fileOut):
  system = open(fileIn,'r').read()
  for key in Pdict.keys():
    system = system.replace(key,str(Pdict[key]))
  fout = open(fileOut,'w')
  fout.write(system)
  return
