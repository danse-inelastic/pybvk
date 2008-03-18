#!/usr/bin/env python

import bvk, numpy, scipy.io, pylab
from scipy.optimize import fmin_powell

numpy.set_printoptions(precision=16)

dosdata = scipy.io.read_array('/usr/local/home/daniel/projects/surf/bvk/data/dos.0010')

data = []

def freq(p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16):
    """ freq() defines the model 
    whose sixteen parameters are optimized
    """

    bb = bvk.getbb([p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16])
    n, ql, wl = bvk.getq(80)
    ql = numpy.pi*ql
    maxFreq = dosdata[-1,0]
    nBins=dosdata.shape[0]
    bincounts = numpy.zeros(nBins)
    for q, w in zip(ql,wl):
        ev = numpy.sqrt(bvk.getdqv(bb,*q));
        c, e = numpy.histogram(ev, dosdata[:,0], range=(0,maxFreq))
        bincounts += w*c
    for i in xrange(nBins-1):
        freq = bincounts / (sum(bincounts) * (dosdata[i+1,0]-dosdata[i,0]))
    return freq

def residuals(p, y):
    """residuals() defines the least-squares function
    being optimized.
    """

    p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16 = p
    print p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16
    data.append([p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16])
    return numpy.sum((y - freq(p1, p2, p3, p4, p5, p6, p7, p8 ,p9, p10, p11, p12, p13, p14, p15, p16))**2)

def l2optimizer():
    """l2optimizer() sets up the optimization 
    of residuals() using Powell's level set method.
    """

    pguess1 = 17.5837
    pguess2 = 18.9758
    pguess3 = -0.3911
    pguess4 = 0.9751
    pguess5 = -0.6105
    pguess6 = 0.5930
    pguess7 = 0.3782
    pguess8 = 0.3019
    pguess9 = -0.1196
    pguess10 = 0.3855
    pguess11 = 0.5165
    pguess12 = -0.2183
    pguess13 = -0.0852
    pguess14 = -0.0390
    pguess15 = 0.0061
    pguess16 = 0.0143

    optimal = fmin_powell(residuals,[pguess1, pguess2, pguess3, pguess4, pguess5, pguess6, pguess7, pguess8, pguess9, \
    pguess10, pguess11, pguess12, pguess13, pguess14, pguess15, pguess16],args=(dosdata[:,1],), full_output=0)
    print optimal

l2optimizer()

scipy.io.write_array('powell', data, precision=16)
