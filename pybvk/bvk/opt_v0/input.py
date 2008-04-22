#!/usr/bin/env python

#==============================================================================
# User input here:
#-----------------------------------------------------------------------------
fcnames = ['FC01', 'FC02', 'FC03', 'FC04', 'FC05', 'FC06', 'FC07', 'FC08', \
           'FC09', 'FC10', 'FC11', 'FC12', 'FC13']
fcs     = [ 16.88,  15.01,  14.63,   0.55,   0.92,   0.69,  -0.57,  -0.12, \
            0.007,   0.03,   0.52,  -0.29,   0.32]

expFile     = "dos.exp"         # in THz, constant binwidth
resFile     = "instrument.res"  # in THz, same binwidth as DOS, from 
                                # negative last data value to last data value.
sysDir      = "./sys-gen/"
sysTemplate = "myFe.tplt"
sysName     = "myFe"
withVecs    = 0
node        = "n00"
maxIter     = 100
randomize   = 0.3               # Apply 30% random noise to initial fcs
#==============================================================================
