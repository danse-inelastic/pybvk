#!/usr/bin/python

def perl2py(inStr):
  return inStr.replace(";","")\
              .replace("perl -w","python")\
              .replace("use System","import System\nfrom math import sqrt\n")\
              .replace("my ","")\
              .replace("$","")\
              .replace("::",".")


import sys

filein  = sys.argv[1]
fileout = sys.argv[2]

fin  = open(filein,'r').read()
fout = open(fileout,'w')
fout.write( perl2py(fin) )
fout.close()

import os
os.system("chmod 755 "+fileout)

