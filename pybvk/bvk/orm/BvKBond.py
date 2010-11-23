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

    A = InvBase.d.int(name='A', label='Atom 1 index')
    A.tip = 'Index of atom 1 of the bond in the atom list of the atomic structure'
    A.help = 'A bond has two atoms. This is for the first atom in the bond. You will need to input the index of this atom in the list of all atoms in the unit cell (index starts from 0 and ends with N_atoms-1)'
    
    B = InvBase.d.int(name='B', label='Atom 2 index')
    B.tip = 'Index of atom 2 of the bond in the atom list of the atomic structure'
    B.help = 'A bond has two atoms. This is for the second atom in the bond. You will need to input the index of this atom in the list of all atoms in the unit cell (index starts from 0 and ends with N_atoms-1)'

    Boffset = InvBase.d.array(
        name='Boffset', 
        elementtype='float',
        default=[0,0,0], shape=3)
    Boffset.label = 'Atom 2 offset'
    Boffset.tip = 'Offset vector of atom 2 relative to its canonical position defined in the atomic structure'
    Boffset.help = 'A bond has two atoms. This is for the second atom in the bond. You will need to input the offset of the atom 2 relative to its canonical position inside the unitcell'

    Boffset_is_fractional = InvBase.d.bool(name='Boffset_is_fractional', default=0)
    Boffset_is_fractional.label = 'Atom 2 offset is fractional'
    Boffset_is_fractional.tip = 'When set, the offset vector of atom 2 is in fractional coordinates. Otherwise, it is in cartesian coordinates'

    force_constant_matrix = InvBase.d.array(
        name='force_constant_matrix', elementtype='float',
        default=[0,0,0,0,0,0,0,0,0,], shape=(3,3))


    dbtablename = 'bvkbonds'


BvKBond.Inventory = Inventory

# version
__id__ = "$Id$"

# End of file 
