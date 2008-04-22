#!/usr/bin/env python

from symmetries import *

#=============================================================================
# Cubic:
#-----------------------------------------------------------------------------
# S = [ C_4y, C_4x, R_x ]
# fn = 'cubic'
#-----------------------------------------------------------------------------


#=============================================================================
# HCP:
#-----------------------------------------------------------------------------
# S = [ C_3z , R_z, R_y ]
# fn = 'hcp'
#-----------------------------------------------------------------------------

#=============================================================================
# FCT == Face Centered Tetragonal:
#-----------------------------------------------------------------------------
S = [ C_4z, C_2x, I ]
fn = 'fct'
#-----------------------------------------------------------------------------

S = closeSyms(S)
writeSyms(S,filename=fn)
