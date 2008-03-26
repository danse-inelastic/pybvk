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
PACKAGE = tests

include local.def

PROJ_CLEAN += $(PROJ_CPPTESTS)

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
hello: hello.cc $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ hello.cc $(PROJ_LIBRARIES)

# version
# $Id$
# End of file
