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


from bvk.find_force_constant_tensor_constraints import symmetryRestricted3X3Tensor, symmetriesRestricted3X3Tensor, findForceContantTensorConstraints, T


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        R = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        restrictions = symmetryRestricted3X3Tensor(R)
        assert restrictions[T[0,0]] == T[1,1]
        assert restrictions[T[0,1]] == T[1,0]
        assert restrictions[T[2,0]] == -T[2,1]
        assert restrictions[T[0,2]] == -T[1,2]
        return


    def test2(self):
        R = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        restrictions = symmetriesRestricted3X3Tensor([R])
        assert restrictions[T[0,0]] == T[1,1]
        assert restrictions[T[0,1]] == T[1,0]
        assert restrictions[T[2,0]] == -T[2,1]
        assert restrictions[T[0,2]] == -T[1,2]
        return


    def test3(self):
        R1 = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        R2 = [
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0],
            ]
        restrictions = symmetriesRestricted3X3Tensor([R1, R2])
        self.assertEqual(restrictions[T[0,0]], T[2,2])
        self.assertEqual(restrictions[T[1,1]], T[2,2])
        self.assertEqual(restrictions[T[0,1]], 0)
        self.assertEqual(restrictions[T[0,2]], 0)
        self.assertEqual(restrictions[T[1,0]], 0)
        self.assertEqual(restrictions[T[1,2]], 0)
        self.assertEqual(restrictions[T[2,0]], 0)
        self.assertEqual(restrictions[T[2,1]], 0)
        return


    # depends on "matter" package
    def test4(self):
        # fcc
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

        #
        from matter.SpaceGroups import sg225
        
        # 110
        vector = [0.5, 0.5, 0]
        print 'bond 110 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 200
        vector = [1,0,0]
        print 'bond 200 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint

        # 211
        vector = [1,0.5,0.5]
        print 'bond 211 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 220
        vector = [1,1,0]
        print 'bond 220 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 310
        vector = [1.5,0.5,0]
        print 'bond 310 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 222
        vector = [2,2,2]
        print 'bond 222 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 321
        vector = [3,2,1]
        print 'bond 321 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 400
        vector = [4,0,0]
        print 'bond 400 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        return


    def test5(self):
        # bcc
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

        #
        from matter.SpaceGroups import sg229
        
        # 111
        vector = [1, 1, 1]
        print 'bond 111 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 200
        vector = [2,0,0]
        print 'bond 200 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint

        # 220
        vector = [2,2,0]
        print 'bond 220 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 311
        vector = [3,1,1]
        print 'bond 311 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 222
        vector = [2,2,2]
        print 'bond 222 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 400
        vector = [4,0,0]
        print 'bond 400 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 133
        vector = [1,3,3]
        print 'bond 133 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        # 420
        vector = [4,2,0]
        print 'bond 420 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg229):
            print constraint
            
        return


    def test6(self):
        # bcc
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

        #
        from matter.SpaceGroups import sg221
        
        # 011
        vector = [0, 1, 1]
        print 'bond 011 for bcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg221):
            print constraint
            
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
