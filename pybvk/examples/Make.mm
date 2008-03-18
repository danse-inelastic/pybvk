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
PACKAGE = examples

#--------------------------------------------------------------------------
#
all: clean

release: clean
	cvs release .

update: clean
	cvs update .

# version
# $Id$

# End of file
