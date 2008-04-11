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

include local.def

PROJ_OUTS = DOS* Omega2 Polarizations WeightedQ system g.py syms
PROJ_CLEAN += $(PROJ_CPPDEMO) $(PROJ_OUTS)

PROJ_PYDEMO =
PROJ_CPPDEMO = fwd h pd randomQs regularQs printQs \
               printEVs printDOS printSys gpy
PROJ_DEMO = $(PROJ_PYDEMO) $(PROJ_CPPDEMO)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -lbvk -llapack
#--------------------------------------------------------------------------
#
all: $(PROJ_DEMO)

#demo:
#	for demo in $(PROJ_DEMO) ; do $${demo}; done
#
release: clean
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
fwd: system gpy $(SRC_LIBDIR)/fwd.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/fwd.c $(PROJ_LIBRARIES)

h: system $(SRC_LIBDIR)/h.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/h.c $(PROJ_LIBRARIES)

pd: system gpy $(SRC_LIBDIR)/pd.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/pd.c $(PROJ_LIBRARIES)

randomQs: system $(SRC_LIBDIR)/randomQs.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/randomQs.c $(PROJ_LIBRARIES)

regularQs: system $(SRC_LIBDIR)/regularQs.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/regularQs.c $(PROJ_LIBRARIES)

printQs: system $(SRC_LIBDIR)/printQs.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/printQs.c $(PROJ_LIBRARIES)

printEVs: system $(SRC_LIBDIR)/printEVs.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/printEVs.c $(PROJ_LIBRARIES)

printDOS: system $(SRC_LIBDIR)/printDOS.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/printDOS.c $(PROJ_LIBRARIES)

printSys: system $(SRC_LIBDIR)/printSys.c $(BLD_LIBDIR)/libbvk.$(EXT_SAR)
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ $(SRC_LIBDIR)/printSys.c $(PROJ_LIBRARIES)

gpy:
	$(CP) $(SRC_LIBDIR)/g.py .

system:
	$(LN_S) $(SRC_SYSDIR)/syms ./syms
	$(PYTHON) $(SRC_SYSDIR)/Al
#	$(RM_F) ./syms


# version
# $Id$
# End of file
