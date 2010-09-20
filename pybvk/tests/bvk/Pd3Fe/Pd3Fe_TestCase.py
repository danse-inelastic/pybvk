#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

skip = True


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        # the structure
        import matter

        atom0 = matter.Atom('Fe', mass=57)
        atom1 = matter.Atom('Pd', (0.5,0.5,0))
        atom2 = matter.Atom('Pd', (0,0.5,0.5))
        atom3 = matter.Atom('Pd', (0.5,0,0.5))
        atoms = [atom0, atom1, atom2, atom3]

        # a = 3.701
        a = 2.
        lattice = matter.Lattice(a=a, b=a, c=a, alpha=90, beta=90, gamma=90)
        struct = matter.Structure(atoms=atoms, lattice=lattice, sgid=221)

        # the model
        from bvk.BvKModel import BvKModel
        from bvk.BvKBond import BvKBond
        model = BvKModel(
            matter = struct,
            uses_primitive_unitcell = 0,
            )

        # the bonds
        # 1nn
        fcm1nnFePd = [
            1.2682470575527145, 0.00, 0.00,
            0.00,  26.016714720313175,  18.162975610029132,
            0.00,  18.162975610029132,  26.016714720313175,
            ]
        model.addBond(
            A=0, B=2,
            force_constant_matrix = fcm1nnFePd,
            )
        model.addBond(
            A=2, B=0,
            force_constant_matrix = fcm1nnFePd,
            )
        
        fcm1nnPdPd = [
            46.406513, 54.794806, 0.00,
            59.731856, 46.406513, 0.00,
            0.00,  0.00, -6.391135,
            ]
        model.addBond(
            #A=2, B=3,  # this gives (-0.5, 0.5, 0) bond and gives a slightly different dos
            A=2, B=3,  Boffset=(0,1,0), Boffset_is_fractional=1, # this works
            #A=1, B=1, Boffset=(0.5,0.5,0), Boffset_is_fractional=1, # this works too
            force_constant_matrix = fcm1nnPdPd,
            )

        # 2nn
        fcm2nnFeFe = [
            -16.875965980649628, 0.00, 0.00,
            0.00,  -16.875965980649628, 0.00,
            0.00, 0.00,  6.5877296391639888,
            ]
        model.addBond(
            A=0, B=0, Boffset = (0,0,1), Boffset_is_fractional=1,
            force_constant_matrix = fcm2nnFeFe,
            )

        fcm2nnPdPd = [
            -1.000528, 0.00, 0.00,
            0.00,-1.733573, 0.00,
            0.00, 0.00, 4.485725,
            ]
        model.addBond(
            A=1, B=1, Boffset = (0,0,1), Boffset_is_fractional=1,
            force_constant_matrix = fcm2nnPdPd,
            )

        fcm2nnPdPd = [
            3.986490, 0.00, 0.00,
            0.00,-0.457419, 0.00,
            0.00, 0.00,-0.457419,
            ]
        model.addBond(
            A=1, B=1, Boffset = (1,0,0), Boffset_is_fractional=1,
            force_constant_matrix = fcm2nnPdPd,
            )
        
        from bvk._utils import _systemFromModel
        cell1, atoms1, sites1, bonds1, symRs1 = _systemFromModel(model)
        from original.pd3fe import cell, atoms, sites, bonds

        from numpy.testing import assert_array_almost_equal
        assert_array_almost_equal(cell, cell1)
        # assert_array_almost_equal(atoms, atoms1)
        assert_array_almost_equal(sites, sites1)
        for bond, bond1 in zip(bonds, bonds1):
            assert_array_almost_equal(bond, bond1)

        from bvk import systemFromModel
        systemFromModel(model, filename='pd3fe')
        import os
        cmd = 'bvkdos.py -N 40 -d 0.1 pd3fe'
        if (os.system(cmd)): raise RuntimeError, "%r failed" % cmd

        cmd = 'plotdos.py'
        if (os.system(cmd)): raise RuntimeError, "%r failed" % cmd
        
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
