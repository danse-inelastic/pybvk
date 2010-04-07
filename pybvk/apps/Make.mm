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
PACKAGE = apps

include local.def

EXPORT_BINS1 = \
	bvkdisps \
	bvkpartialdos \
	bvkrandomQs \
	bvkregularQs \


EXPORT_PYAPPS = \
	bvkdisp.py \
	bvkdos.py \
	plotdos.py \


EXPORT_BINS = $(EXPORT_PYAPPS) $(EXPORT_BINS1)


PROJ_CLEAN += $(EXPORT_BINS1)


#--------------------------------------------------------------------------
#
all:  export

release: clean
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

bvkpartialdos: ../examples/pd
	$(CP) ../examples/pd bvkpartialdos

bvkdisps: ../examples/h
	$(CP) ../examples/h bvkdisps

bvkrandomQs: ../examples/randomQs
	$(CP) ../examples/randomQs bvkrandomQs

bvkregularQs: ../examples/regularQs
	$(CP) ../examples/regularQs bvkregularQs


export:: $(EXPORT_BINS) export-binaries



# version
# $Id$
# End of file
