#!/usr/bin/env python

import os
import numpy, io, template2sys as t2s
numpy.set_printoptions(precision=16)
nar = numpy.add.reduce

# normalize a density of states to 1.0
def normalize(x,y,err,val=1.0):
  dx = x[1] - x[0]
  y /= nar(y)*dx
  y *= val        
  # Do something with errors.
  return x,y,err

# take two lists, make a dictionary.
def dictFromLists(a,b):
  res = {}
  for i in range(len(a)):
    res[a[i]] = b[i]
  return res

# make the function that takes fcs and produces a DOS.
def make_getDOS(ps,fcnames,sysDir,sysTemplate,sysName,binWidth,resFile):
  global withVecs, node
  runBvK      = " ".join(["b",node,sysName,str(withVecs),str(binWidth)])
  convolve    = " ".join(["convolve.py","DOS",resFile])
  def getDOS(fcs):
    print "FCS:", fcs
    ps.append( dictFromLists(fcnames,fcs) )
    t2s.toSys(ps[-1], sysDir + sysTemplate, sysDir + sysName)
    os.system("chmod 755 " + sysDir + sysName)
    os.system(runBvK)
    os.system(convolve)
    E,D,R = io.load("DOS.conv")
    if D[0] < 0.0:
      print "That's negative, dude!"
      D = numpy.zeros( e.shape ) + 1e20
    else:
      E,D,R = normalize(E,D,R)
    return E,D,R
  return getDOS

# make the function that calculates the least squares penalty
def make_penalty(d,getDOS):
  def penalty(fcs):
    return nar(   (d - getDOS(fcs)[1] )**2    )
  return penalty

# Call scipy's optimizer.
def l2optimizer(penalty,fcs,maxIter):
    """l2optimizer() sets up the optimization of penalty() using Powell's 
       level set method.  """
    from scipy.optimize import fmin_powell
    optimal = fmin_powell(penalty,fcs,full_output=0,maxiter=maxIter)
    print optimal

# input and normalize the experimental DOS.  Get its binwidth.
def setupDos(expFile,randomize):
  e,d,r       = io.load(expFile)
  e,d,r       = normalize(e,d,r)
  binWidth    = e[1] - e[0]
  return d,binWidth

# Randomize the force constant array
def setupFcs(fcs,randomize):
  R =  ( 0.5 - numpy.random.random(len(fcs)) )*(2.0*randomize)
  return (  ( 1.0 + R ) * fcs ).tolist()

def run():
  global fcnames, fcs, expFile, resFile
  global sysDir, sysTemplate, sysName
  global maxIter, randomize
  ps = []
  d,binWidth = setupDos(expFile,randomize) 
  fcs = setupFcs(fcs,randomize)
  getDOS = make_getDOS(ps,fcnames,sysDir,sysTemplate,sysName,binWidth,resFile)
  penalty = make_penalty(d,getDOS)
  l2optimizer(penalty,fcs,maxIter)
  return

if __name__ == '__main__':
  os.system("date")
  from input import *  # get user input
  run()
  os.system("date")
