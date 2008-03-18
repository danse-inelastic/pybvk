# -*- Makefile -*-
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
PROJECT = bvk
PACKAGE = _bvk
MODULE = _bvk
#PACKAGE = bvkmodule
#MODULE = bvk

include std-pythonmodule.def
include local.def

#PROJ_CXX_SRCLIB = -llapack -lbvk
PROJ_CXX_SRCLIB = -lbvk

PROJ_SRCS = \
    bindings.cc \
    exceptions.cc \
    misc.cc \
#   _bvk.cc


# version
# $Id$
# End of file
