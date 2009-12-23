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


from BvKBond import BvKBond

class BvKModel(object):

    matter = None
    uses_primitive_unitcell = 1 # use the primitive unitcell of matter structure if true
    
    short_description = ''
    bonds = []

    long_description = ''
    reference = ''
    
    
# version
__id__ = "$Id$"

# End of file 
