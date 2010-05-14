#!/usr/bin/python
#Created by FCS2MySystem.py from
#/home/lmauger/BvKAnalysis/pybvk/branches/DynModels/20100310_Pd3Fe_PdFixed_24x0/optimize/fcs.csv

from math import sqrt

# This is adapted from the Ni input example to suit the L12 structure
# L12 has majority atom on faces and minority atom of cubic lattice positions


# a scales lattice vectors
# Here a is half the fe-fe nearest nearest neighbor distance

a=1.0

# Weight of each variety of atom
# Work on legitimate sig figs

#mFe=    9.2734972e-26
mFe57 = 9.5434588e-26
mPd=    1.7671870e-25


# We will choose the conventional simple cubic unit cell with a basis
# Our cell has coordinates that fit in a conventional cartesian system
cell = [
    2*a,   0,   0,
    0, 2*a,   0,
    0,   0, 2*a
    ]

atoms=[
    [ "Fe57", mFe57 ],
    [   "Pd",   mPd ],
    ]

sites=[
    [ 0.0*a, 0.0*a, 0.0*a,0 ],
    [ 1.0*a, 1.0*a, 0.0*a,1 ],
    [ 0.0*a, 1.0*a, 1.0*a,1 ],
    [ 1.0*a, 0.0*a, 1.0*a,1 ],
    ]

# These initial bond matrices were provided by Mike Winterrose's
# Phon calculations of the Pd3Fe structure.  I used Phon output converted
# to N/m and multiplied by -1 to get these values below.

# The Phon code and I differ on which bonds are the 5th nearest
# neighbors. I don't use Mike's 5NN because they are actually the 6NN.
# I should test to see if these are important eventually.



bonds=[
    #1NN
    #FC3
    [ 0,1,  0*a,1*a,1*a,     1.2682470575527145, 0.00, 0.00,
      0.00,  26.016714720313175,  18.162975610029132,
      0.00,  18.162975610029132,  26.016714720313175 ],
    
    [ 1,0, 0*a,-1*a,-1*a,    1.2682470575527145, 0.00, 0.00,
      0.00,  26.016714720313175,  18.162975610029132,
      0.00,  18.162975610029132,  26.016714720313175 ],
    #FC4 Pd3Fe_lsInterp_24GPa_fcs.csv
    [ 1,1, 1*a,1*a,0*a,      46.406513, 54.794806, 0.00,
      59.731856, 46.406513, 0.00,
      0.00,  0.00, -6.391135],
    # the following bond to me is identical to the previous one. but if
    # it is used in place of the previous one, it gives different result
    # for DOS
    ##   [ 1,1, -1*a,1*a,0*a,      46.406513, 59.731856, 0.00,
    ##     54.794806, 46.406513, 0.00,
    ##     0.00,  0.00, -6.391135],
    
    #2NN
    #FC5
    [ 0,0, 0*a,0*a,2*a,       -16.875965980649628, 0.00, 0.00,
      0.00,  -16.875965980649628, 0.00,
      0.00, 0.00,  6.5877296391639888
      ],
    #FC6 Pd3Fe_lsInterp_24GPa_fcs.csv
    [ 1,1, 0*a,0*a,2*a,     -1.000528, 0.00, 0.00,
      0.00,-1.733573, 0.00,
      0.00, 0.00, 4.485725],
    
    #  There is no way to distinguish this bond from the one above
    #  without resorting to labeling specific atoms
    #  Had negative FCMatrix until 9/23/09
    #FC7 Pd3Fe_lsInterp_24GPa_fcs.csv
    [ 1,1, 2*a,0*a,0*a,      3.986490, 0.00, 0.00,
      0.00,-0.457419, 0.00,
      0.00, 0.00,-0.457419],
    
    #3NN
    #FC8
    #  [ 0,1, 2*a,1*a,1*a,      FC15, 0.00, 0.00,
    #                           0.00, FC16, FC17,
    #                           0.00, FC17, FC16 ],
    #  [ 1,0, -2*a,-1*a,-1*a,   FC15, 0.00, 0.00,
    #                           0.00, FC16, FC17,
    #                           0.00, FC17, FC16 ],
    #FC9
    # Bad value in matrix - 9/23/09
    #  [ 1,1, 1*a,1*a,2*a,      FC18, FC19, 0.00,
    #                           FC20, FC18, 0.00,
    #                           0.00, 0.00, FC21 ],
    #
    #4NN
    #FC10
    #  [ 0,0, 0*a,2*a,2*a,      FC22, 0.00, 0.00,
    #                           0.00, FC23, 0.00,
    #                           0.00, 0.00, FC23 ],
    #FC11
    #  [ 1,1, 0*a,2*a,2*a,      FC24, 0.00, 0.00,
    #                           0.00, FC25, 0.00,
    #                           0.00, 0.00, FC25 ],
    #
    #This next one may not be a distinct bond - may require atom labeling
    #FC12
    #  [ 1,1, 2*a,0*a,2*a,      FC26, 0.00, 0.00,
    #                           0.00, FC27, 0.00,
    #                           0.00, 0.00, FC28 ],
    #5NN- The 5th NN don't agree with mikes at all
    # but I am right - but that means I have no values
    #  [ 0,1, 3*a,1*a,0*a,            -0.085, -0.035,  0.000,
    #                                 -0.035,  0.007,  0.000,
    #                                  0.000,  0.000,  0.018 ],
    #  [ 1,0, -3*a,-1*a,0*a,            -0.085, -0.035,  0.000,
    #                                 -0.035,  0.007,  0.000,
    #                                  0.000,  0.000,  0.018 ],
    #  [ 1,1, 3*a,1*a,0*a,            -0.085, -0.035,  0.000,
    #                                 -0.035,  0.007,  0.000,
    #                                  0.000,  0.000,  0.018 ],
    #
    #6NN - Mikes 5NN
    #  [ 0,0, 2*a,2*a,2*a,     FC29, 0.00, 0.00,
    #                          0.00, FC29, 0.00,
    #                          0.00, 0.00, FC29 ],
    #  [ 1,1, 2*a,2*a,2*a,     FC30, 0.00, 0.00,
    #                          0.00, FC31, 0.00,
    #                          0.00, 0.00, FC31 ],
    ]

if __name__ == '__main__': 
    import System
    System.write(cell,atoms,sites,bonds,"cubic")
