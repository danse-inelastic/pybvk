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


    def __init__(
        self, matter=None, bonds=[],
        short_description='', long_description='',
        reference = '',
        uses_primitive_unitcell = True
        ):
        self.matter = matter
        self.uses_primitive_unitcell = uses_primitive_unitcell
        self.short_description = short_description
        self.bonds = bonds
        self.long_description = long_description
        self.reference = reference
        return
    

    def addBond(self, A, B, force_constant_matrix,
                Boffset=(0,0,0), Boffset_is_fractional=0):
        'create a new bond'
        from BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = self.matter
        bond.uses_primitive_unitcell = self.uses_primitive_unitcell
        bond.A = A
        bond.B = B
        bond.force_constant_matrix = force_constant_matrix
        bond.Boffset_is_fractional = Boffset_is_fractional
        bond.Boffset = Boffset
        self.bonds.append(bond)
        return bond


    def copy(self):
        bonds = [bond.copy() for bond in self.bonds]
        copy = self.__class__(
            matter=self.matter,
            uses_primitive_unitcell = self.uses_primitive_unitcell,
            short_description = self.short_description,
            bonds = bonds,
            long_description = self.long_description,
            reference = self.reference,
            )
        return copy
    
    
# version
__id__ = "$Id$"

# End of file 
