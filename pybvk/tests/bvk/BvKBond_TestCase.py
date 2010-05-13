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
        import matter
        lattice = matter.Lattice(a=3.701, b=3.701, c=3.701, alpha=90, beta=90, gamma=90)
        atom1 = matter.Atom('C')
        atom2 = matter.Atom('H', [0.5, 0.5, 0])
        atom3 = matter.Atom('H', [0.5, 0, 0.5])
        atom4 = matter.Atom('H', [0, 0.5, 0.5])
        struct = matter.Structure([atom1, atom2, atom3, atom4], lattice=lattice, sgid=221)

        from bvk.BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = struct
        bond.uses_primitive_unitcell = 0
        bond.A = 0
        bond.B = 1
        bond.Boffset = [0,0,0.]
        bond.Boffset_is_fractional = 1
        
        # 110
        print 'bond 00.50.5 for sc lattice'
        constraints = bond.getConstraints()
        #constraints = [str(c) for c in constraints]

        self.assertEqual(len(constraints), 6)
        
        from bvk.find_force_constant_tensor_constraints import T
        # m12 = m21
        self.assertAlmostEqual(constraints[0][0]/T[0,1], 1)
        self.assertAlmostEqual(constraints[0][1]/T[1,0], 1)
        # m32 = 0
        self.assertAlmostEqual(constraints[1][0]/T[2,0], 1)
        self.assertAlmostEqual(constraints[1][1], 0)
        # m11 = m22
        self.assertAlmostEqual(constraints[2][0]/T[0,0], 1)
        self.assertAlmostEqual(constraints[2][1]/T[1,1], 1)
        # m23 = 0
        self.assertAlmostEqual(constraints[3][0]/T[1,2], 1)
        self.assertAlmostEqual(constraints[3][1], 0)
        # m13 = 0
        self.assertAlmostEqual(constraints[4][0]/T[0,2], 1)
        self.assertAlmostEqual(constraints[4][1], 0)
        # m32 = 0
        self.assertAlmostEqual(constraints[5][0]/T[2,1], 1)
        self.assertAlmostEqual(constraints[5][1], 0)
            
        return
    
    

def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
