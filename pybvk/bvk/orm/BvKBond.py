# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from bvk.BvKBond import BvKBond


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    from matter.orm.Structure import Structure
    matter = InvBase.d.reference(name='matter', targettype=Structure, owned=0)
    uses_primitive_unitcell = InvBase.d.bool(name='uses_primitive_unitcell', default=1)

    A = InvBase.d.int(name='A')
    A.help = 'Index of atom A in the atom list in the atomic structure'
    
    B = InvBase.d.int(name='B')
    B.help = 'Index of atom B in the atom list in the atomic structure'

    Boffset = InvBase.d.array(
        name='Boffset', elementtype='float',
        default=[0,0,0], shape=3)
    Boffset.help = 'Offset vector of atom B relative to its canonical position defined in the atomic structure'
    
    Boffset_is_fractional = InvBase.d.bool(name='Boffset_is_fractional', default=0)
    Boffset_is_fractional.tip = 'When set, the offset vector of atom B is in fractional coordinates. Otherwise, it is in cartesian coordinates'

    force_constant_matrix = InvBase.d.array(
        name='force_constant_matrix', elementtype='float',
        default=[0,0,0,0,0,0,0,0,0,], shape=(3,3))


    dbtablename = 'bvkbonds'


BvKBond.Inventory = Inventory

# version
__id__ = "$Id$"

# End of file 
