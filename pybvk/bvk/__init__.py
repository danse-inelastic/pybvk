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

# import bvk python functions defined in C binding layer
from _bvk import *  #XXX building with Makefile
#from bvk import *   #XXX building with Make.mm

def copyright():
    return "bvk module: Copyright (c) 2008 Mike McKerns";


# version
__id__ = "$Id$"

#  End of file 
