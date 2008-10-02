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
PACKAGE = bvk

BUILD_DIRS = \
	input_generators \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#
all: export
	BLD_ACTION="export" $(MM) recurse

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py

export:: export-python-modules

# version
# $Id$
# End of file
