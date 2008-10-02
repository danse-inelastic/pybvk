# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                    Jiao Lin     
#                        California Institute of Technology
#                          (C) 2008  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = bvk
PACKAGE = input_generators/system

BUILD_DIRS = \

OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="export" $(MM) recurse

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    System.py \
    __init__.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id$

# End of file
