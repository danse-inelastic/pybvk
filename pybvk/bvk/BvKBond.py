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
    uses_primitive_unitcell = 1 # use the primitive unitcell of matter structure if true. must be consistent with the setting in bvk model.

    # settable by users
    A = 0 # index of atom A in the atom list in the atomic structuree
    B = 0 # index of atom B in the atom list in the atomic structuree 
    Boffset = [0,0,0] # offset vector for atom B. it should be in cartesian or fractional coords, depending on Boffset_is_fractional
    Boffset_is_fractional = 1 # offset vector is in fractional coords if true
    force_constant_matrix = [[0,0,0], [0,0,0], [0,0,0]] # force constant matrix in cartesian coords


    def __str__(self):
        return 'bond: atom %s to atom % shifted %s:\n%s' % (
            self.A, self.B, self.Boffset, numpy.array(self.force_constant_matrix))


    def getBondVectorInCartesianCoords(self):
        # the method for converting to cartesian depends on the flag "uses_primitive_unitcell"
        if self.uses_primitive_unitcell:
            cartesian = self.matter.primitive_unitcell.cartesian
        else:
            cartesian = self.matter.lattice.cartesian

        # offset
        Boffset = self.Boffset
        if self.Boffset_is_fractional:
            Boffset = cartesian(Boffset)

        #
        A = self.A; B = self.B
        if self.uses_primitive_unitcell:
            atoms = self.matter.primitive_unitcell.atoms
        else:
            atoms = self.matter
            
        vec = cartesian(atoms[B].xyz-atoms[A].xyz)
            
        return Boffset + vec
        


    def getBondVectorInLatticeFractionalCoords(self):
        # the method for converting to cartesian depends on the flag "uses_primitive_unitcell"
        if self.uses_primitive_unitcell:
            cartesian = self.matter.primitive_unitcell.cartesian
        else:
            cartesian = self.matter.lattice.cartesian

        # offset
        Boffset = self.Boffset
        if self.Boffset_is_fractional:
            Boffset = cartesian(Boffset)
        # convert to fractional coords in the lattice (which could be not-primitive)
        Boffset = self.matter.lattice.fractional(Boffset)

        #
        A = self.A; B = self.B
        if self.uses_primitive_unitcell:
            atoms = self.matter.primitive_unitcell.atoms
            vec = self.matter.lattice.fractional(cartesian(atoms[B].xyz-atoms[A].xyz))
        else:
            atoms = self.matter
            vec = atoms[B].xyz - atoms[A].xyz
            
        return Boffset + vec
    

    def getConstraints(self):
        vector = self.getBondVectorInLatticeFractionalCoords()
        lattice = self.matter.lattice
        sg = self.matter.sg
        from bvk.find_force_constant_tensor_constraints import findForceContantTensorConstraints
        return findForceContantTensorConstraints(vector, lattice, sg)


import numpy


# version
__id__ = "$Id$"

# End of file 
