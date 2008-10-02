# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = bvk/syms
PACKAGE = 

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
# export

EXPORT_ETC = \
	cubic \
	fct \
	hcp \

export:: export-etc

# version
# $Id: Make.mm,v 1.1.1.1 2006-11-27 00:09:51 aivazis Exp $

# End of file
