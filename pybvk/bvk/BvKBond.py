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
    A = 0
    B = 0
    Boffset = [0,0,0]
    force_constant_matrix = [[0,0,0], [0,0,0], [0,0,0]]


    def __str__(self):
        return 'bond: atom %s to atom % shifted %s:\n%s' % (
            self.A, self.B, self.Boffset, self.force_constant_matrix)


# version
__id__ = "$Id$"

# End of file 
