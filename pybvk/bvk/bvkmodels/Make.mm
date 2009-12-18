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
PACKAGE = bvkmodels

BUILD_DIRS = \
    formatted \

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
	converttobvkmodelobject.py \
	__init__.py \
	ag_293.py \
	ag_296.py \
	al_300.py \
	al_80.py \
	au_295.py \
	ce_295.py \
	co_297.py \
	cr_300.py \
	cu_1336.py \
	cu_296.py \
	cu_49.py \
	cu_673.py \
	cu_80.py \
	cu_973.py \
	fe_295.py \
	ho_298.py \
	in_77.py \
	k_9.py \
	li_293.py \
	li_98.py \
	mg_290.py \
	mo_296.py \
	na_90.py \
	nb_296.py \
	ni_296.py \
	ni_298.py \
	ni_676.py \
	pb_80.py \
	pd_120.py \
	pd_296.py \
	pd_673.py \
	pd_853.py \
	pt_90.py \
	rb_12.py \
	rb_120.py \
	rb_205.py \
	rb_85.py \
	sc_295.py \
	ta_296.py \
	tb_298.py \
	th_296.py \
	ti_295.py \
	tl_296.py \
	tl_77.py \
	v_296.py \
	w_298.py \
	y_295.py \
	zn_80.py \
	zr_295.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id$

# End of file
