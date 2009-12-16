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
	__init__.py \
	bvk_ag_293.py \
	bvk_ag_296.py \
	bvk_al_300.py \
	bvk_al_80.py \
	bvk_au_295.py \
	bvk_ce_295.py \
	bvk_co_297.py \
	bvk_cr_300.py \
	bvk_cu_1336.py \
	bvk_cu_296.py \
	bvk_cu_49.py \
	bvk_cu_673.py \
	bvk_cu_80.py \
	bvk_cu_973.py \
	bvk_fe_295.py \
	bvk_ho_298.py \
	bvk_in_77.py \
	bvk_k_9.py \
	bvk_li_293.py \
	bvk_li_98.py \
	bvk_mg_290.py \
	bvk_mo_296.py \
	bvk_na_90.py \
	bvk_nb_296.py \
	bvk_ni_296.py \
	bvk_ni_298.py \
	bvk_ni_676.py \
	bvk_pb_80.py \
	bvk_pd_120.py \
	bvk_pd_296.py \
	bvk_pd_673.py \
	bvk_pd_853.py \
	bvk_pt_90.py \
	bvk_rb_12.py \
	bvk_rb_120.py \
	bvk_rb_205.py \
	bvk_rb_85.py \
	bvk_sc_295.py \
	bvk_ta_296.py \
	bvk_tb_298.py \
	bvk_th_296.py \
	bvk_ti_295.py \
	bvk_tl_296.py \
	bvk_tl_77.py \
	bvk_v_296.py \
	bvk_w_298.py \
	bvk_y_295.py \
	bvk_zn_80.py \
	bvk_zr_295.py \


export:: export-package-python-modules
	BLD_ACTION="export" $(MM) recurse

# version
# $Id$

# End of file
