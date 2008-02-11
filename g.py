#!/usr/bin/python

import sys
sys.path.append("/home/mkresch/src/inelastic/idf")
import DOS

files = sys.argv[1:]

import Gnuplot
g = Gnuplot.Gnuplot()
gd = Gnuplot.Data

for i in files:
  D = DOS.read(filename=i)
  g.replot(gd(D[1],D[2],with='l lw 4'))

raw_input("Press <Enter> to close up shop...")
