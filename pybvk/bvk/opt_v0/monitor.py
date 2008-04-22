#!/usr/bin/env python

import Gnuplot
g = Gnuplot.Gnuplot()
gd = Gnuplot.Data
g('set grid')
g('set xzeroaxis -1')
g('set xrange [0:12]')

import io
e,d,r = io.load("dos.exp")

next = ''
print "q to quit."
while next != 'q' :
  E,D,R = io.load("DOS.conv")
  g.plot(gd(e,d,with='p pt 9 lt -1'))
  g.replot(gd(E,D,with='l lw 4 lt 3'))
  next = raw_input()
  
