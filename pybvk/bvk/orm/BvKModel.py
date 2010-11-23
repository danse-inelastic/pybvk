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


from dsaw.model.Inventory import Inventory as InvBase


from matter.orm.Structure import Structure
from BvKBond import BvKBond


class Inventory(InvBase):

    matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[Structure], owned=0)
    uses_primitive_unitcell = InvBase.d.bool(
        name='uses_primitive_unitcell', default=1,
        tip='Please be very careful changing this property. It affects all bonds in this model.',
        )

    short_description = InvBase.d.str(name='short_description', label='description')
    short_description.tip = 'a short description'

    bonds = InvBase.d.referenceSet(name='bonds', targettype=BvKBond, owned=1)

    long_description = InvBase.d.str(name='long_description', label='details', max_length=2048)
    
    reference = InvBase.d.str(name='reference', max_length=1024)
    reference.tip = 'The origin of this model'
    
    dbtablename = 'bvkmodels'

from bvk.BvKModel import BvKModel
BvKModel.Inventory = Inventory

# version
__id__ = "$Id$"

# End of file 
