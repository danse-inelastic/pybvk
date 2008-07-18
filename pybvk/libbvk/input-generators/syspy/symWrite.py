#!/usr/bin/env python

from symmetries import *

try:
  import sys
  symmetry = sys.argv[1]
except:
  symmetry = "None"
#=============================================================================
if symmetry == 'hcp':
  S = [ C_3z , R_z, R_y ]
#=============================================================================
elif symmetry == 'cubic':
  S = [ C_4y, C_4x, R_x ]
#=============================================================================
elif symmetry == 'fct':  # Face Centered Tetragonal:
  S = [ C_4z, C_2x, I ]
#=============================================================================
elif symmetry == 'tet': # T_h (tetrahedral?)
  S = [ C_4y, C_4x ]
#=============================================================================
elif symmetry == 'identity':
  S = [ ]
#=============================================================================
else:  # set to identity
  print "Warning: '%s' not recognized" % symmetry
  print "setting symmetry to 'identity'"
  symmetry = 'identity'
  S = [ ]
#-----------------------------------------------------------------------------

S = closeSyms(S)
writeSyms(S,filename=symmetry)
