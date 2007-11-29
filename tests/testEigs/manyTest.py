#!/usr/bin/python

import os
import sys
import testD

N_b = int(sys.argv[2])

os.system("a " + sys.argv[1])
if testD.test(N_b):
  pass
else:
  raise("Failed matrix # 0")

i = 1

while i < int(sys.argv[3]) :
  os.system(' rm -f dos eigval eigvec freqs D.py *.pyc ')
  os.system(' h 1>tmp.py 2>/dev/null')
  os.system(' echo "import numpy" > D.py')
  os.system(' echo "" >> D.py')
  os.system(' cat tmp.py >> D.py')
  os.system(' echo "" >> D.py')
  os.system(' rm tmp.py')
  if testD.test(N_b):
    sys.stderr.write(".")
    if i%80 == 0:
      sys.stderr.write("\n")
  else:
    raise("Failed matrix # %i" % i)
  i += 1

sys.stderr.write("\n")
