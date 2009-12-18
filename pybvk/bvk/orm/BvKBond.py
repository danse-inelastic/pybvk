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

    A = InvBase.d.int(name='A')
    B = InvBase.d.int(name='B')

    Boffset = InvBase.d.array(
        name='Boffset', elementtype='float',
        default=[0,0,0], shape=3)

    force_constant_matrix = InvBase.d.array(
        name='force_constant_matrix', elementtype='float',
        default=[0,0,0,0,0,0,0,0,0,], shape=(3,3))


    dbtablename = 'bvkbonds'


BvKBond.Inventory = Inventory

# version
__id__ = "$Id$"

# End of file 
