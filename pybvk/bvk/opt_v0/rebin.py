#!/usr/bin/python

# Quick linearly interpolating DOS rebinner.
# Error propagation is _totally_ wrong!

import numpy
      
def l_terp(x0,x1,y0,y1,xf):
  return y0 + (y1-y0)/(x1-x0) * (xf-x0)

def rebin(ei,di,ri,ef):
  df = numpy.zeros(ef.shape)
  rf = numpy.zeros(ef.shape)
  for f in range(len(ef)):
    i = numpy.argmin( (ei - ef[f])**2 )
    if ei[i] == ef[f]:
      df[f] = di[i]
      rf[f] = ri[i]
    elif ei[i] < ef[f]:
      if i+1 < len(ei):
        df[f] = l_terp( ei[i],ei[i+1],di[i],di[i+1],ef[f] )
        rf[f] = l_terp( ei[i],ei[i+1],ri[i],ri[i+1],ef[f] )
      else:
        print "extrapolation"
        df[f] = l_terp( ei[-2],ei[-1],di[-2],di[-1],ef[f] )
        rf[f] = l_terp( ei[-2],ei[-1],ri[-2],ri[-1],ef[f] )
    elif ei[i] > ef[f]:
      if i-1 >= 0: 
        df[f] = l_terp( ei[i-1],ei[i],di[i-1],di[i],ef[f] )
        rf[f] = l_terp( ei[i-1],ei[i],ri[i-1],ri[i],ef[f] )
      else:
        print "extrapolation"
        df[f] = l_terp( ei[0],ei[1],di[0],di[1],ef[f] )
        rf[f] = l_terp( ei[0],ei[1],ri[0],ri[1],ef[f] )
  return df,rf
