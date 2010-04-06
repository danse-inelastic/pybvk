# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Jiao Lin
# linjiao@caltech.edu
# (C) 2010 All Rights Reserved
# 
# <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
PROJECT = bvk
PACKAGE = tests/apps

include local.def

PROJ_CLEAN += $(PROJ_CPPTESTS)
PROJ_TIDY += \
	DOS* \
	Omega2 \
	Polarizations \
	Qgridinfo \
	system \
	WeightedQ \


PROJ_PYTESTS = signon.py
PROJ_CPPTESTS = hello 
PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -lbvk -llapack

#--------------------------------------------------------------------------
#
all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

# version
# $Id$
# End of file
