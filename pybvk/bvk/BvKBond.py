# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class BvKBond(object):

    # should be assigned when created
    matter = None

    # settable by users
    A = 0 # index of atom A in the atom list in the atomic structuree
    B = 0 # index of atom B in the atom list in the atomic structuree 
    Boffset = [0,0,0] # offset vector for atom B. it should be in fractional coords
    force_constant_matrix = [[0,0,0], [0,0,0], [0,0,0]] # force constant matrix in cartesian coords


    def __str__(self):
        return 'bond: atom %s to atom % shifted %s:\n%s' % (
            self.A, self.B, self.Boffset, self.force_constant_matrix)


# version
__id__ = "$Id$"

# End of file 
