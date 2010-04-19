#!/usr/bin/env python
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Mike McKerns
# mmckerns@caltech.edu
# (C) 2008 All Rights Reserved
# 
# <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
__author__='Mike McKerns'
__doc__="""
pybvk: bvk forward engine
"""


try:
    # import bvk python functions defined in C binding layer
    from _bvk import *  #XXX building with Makefile
    #from bvk import *   #XXX building with Make.mm
except ImportError:
    pass
    #import warnings
    #warnings.warn('bvk c binding was not loaded!')



def systemFromModel(model, **kwds):
    from _utils import systemFromModel
    return systemFromModel(model, **kwds)

    

def copyright():
    return "bvk module: Copyright (c) 2008 Mike McKerns";


# version
__id__ = "$Id$"

#  End of file 
