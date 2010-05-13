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


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        # the structure
        import matter

        atom0 = matter.Atom('Fe')
        atom1 = matter.Atom('Pd', (0,0.5,0.5))
        atom2 = matter.Atom('Pd', (0.5,0,0.5))
        atom3 = matter.Atom('Pd', (0.5,0.5,0))
        atoms = [atom0, atom1, atom2, atom3]

        a = 3.701
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
        fcm1nn = [
            1.2682470575527145, 0.00, 0.00,
            0.00,  26.016714720313175,  18.162975610029132,
            0.00,  18.162975610029132,  26.016714720313175,
            ]
        for i in range(1,4):
            model.addBond(
                A=0, B=i,
                force_constant_matrix = fcm1nn,
                )
            model.addBond(
                A=i, B=0,
                force_constant_matrix = fcm1nn,
                )

        fcm1nnPdPd = [
            46.406513, 54.794806, 0.00,
            59.731856, 46.406513, 0.00,
            0.00,  0.00, -6.391135,
            ]
        for i in range(1,4):
            for j in range(1,4):
                if i==j : continue
                model.addBond(
                    A=i, B=j,
                    force_constant_matrix = fcm1nnPdPd,
                    )
        from bvk import systemFromModel
        systemFromModel(model, filename='pd3fe')
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
