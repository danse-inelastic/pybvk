#!/usr/bin/env python

import Gnuplot
import io

def monitor(expFile,convFile):
  g = Gnuplot.Gnuplot()
  gd = Gnuplot.Data
  g('set grid')
  g('set xzeroaxis -1')
  g('set xrange [0:12]')

  e,d,r = io.load(expFile)

  next = ''
  print "q to quit."
  while next != 'q' :
    E,D,R = io.load(convFile)
    g.plot(gd(e,d,with='p pt 9 lt -1'))
    g.replot(gd(E,D,with='l lw 4 lt 3'))
    next = raw_input()
  return


if __name__ == '__main__':
  expFile = "dos.exp"
  convFile = "DOS.conv"
# expFile = sys.argv[-2]
# convFile  = sys.argv[-1]
  monitor(expFile,convFile)
