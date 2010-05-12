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


# find constraints on force constant matrix imposed by crystal symmetry
#

#  
#  * depends on sympy, numpy
#


import numpy

import sympy.matrices as matrices
import sympy
def _matrixelementsymbol(i,j):
    r = sympy.Symbol('m%s%s' % (i+1,j+1))
    return r
T = [ [_matrixelementsymbol(i,j) for j in range(3)] for i in range(3)]
T = matrices.Matrix(T)


def symmetryRestricted3X3Tensor(R):
    """find the restrictions to a 3X3 tensor given the transformation matrix
    of the symmetry operation.
    """
    R = matrices.Matrix(R)
    # R-1 * T * R = T
    equation = R.T * T * R - T
    from sympy.solvers import solve
    import operator
    equation = reduce(operator.add, equation.tolist())
    symbols = reduce(operator.add, T.tolist())
    solution = solve(equation, *symbols)
    return solution


def symmetriesRestricted3X3Tensor(Rs):
    """find the restrictions to a 3X3 tensor given the transformation matrices
    of the symmetry operations.
    """
    equations = _equationsForSymmetriesRestricted3X3Tensor(Rs)

    import operator
    symbols = reduce(operator.add, T.tolist())

    from sympy.solvers import solve
    solution = solve(equations, *symbols)
    
    return solution


def _equationsForSymmetriesRestricted3X3Tensor(Rs):
    Rs = map(matrices.Matrix, Rs)
    # R-1 * T * R = T
    equations = [R.T * T * R - T for R in Rs]
    import operator
    equations = [reduce(operator.add, equation.tolist())
                 for equation in equations]
    equations = [exp_cleaner.render(eq) for eq in equations]
    return reduce(operator.add, equations)
    

# depends on "matter" package
def findForceContantTensorConstraints(vector, lattice, sg):
    """find the restrictions on force constant tensor (3X3) given
    the vector of the bond (in relative lattice coordinates), and
    the symmetry group.

    sg is an instance of matter.SpaceGroups.SpaceGroup. required methods are 'iter_symops_leave_vector_unchanged', which should return symmetry operations that has an attribute 'R' being 3X3 rotation matrix represented in relative lattice coordinates.
    lattice is an instance of matter.Lattice.Lattice. required attribute: 'base', which is the matrix of base vectors in cartesian coordinates.
    vector is a vector of 3 in relative lattice coords
    """
    b = lattice.base
    import numpy.linalg as nl
    binv = nl.inv(b)

    # the equations result from symmetry requirement of the bond
    # the rotation matrices in relative coords
    #   R in Rs don't work: special things about numpy array
    allRs = [symop.R for symop in sg.iter_symops_leave_vector_unchanged(vector)]
    # print allRs
    Rs = []; ids = []
    for R in allRs:
        if id(R) not in ids:
            Rs.append(R)
            ids.append(id(R))
        continue
    # print Rs
    #  function to convert matrix to cartesian
    def toCartesian(R):
        return numpy.dot(numpy.dot(binv, R), b)
    Rs = map(toCartesian, Rs)
    # print Rs
    equations = _equationsForSymmetriesRestricted3X3Tensor(Rs)

    # add the equations for instrisic symmetry of force constant tensor
    equations += _intrinsicSymmetryEquationsForForceConstantTensor

    # the symbols to solve (9 matrix elements)
    import operator
    symbols = reduce(operator.add, T.tolist())

    # solve the equations
    from sympy.solvers import solve
    restrictions = solve(equations, *symbols)
    
    return restrictions.items()


# intrinsic symmetry of force constant tensor
_intrinsicSymmetryEquationsForForceConstantTensor = [
    T[0,1]-T[1,0],
    T[0,2]-T[2,0],
    T[1,2]-T[2,1],
    ]



class SympyExpressionCleaner(object):

    '''
    expression resulted from symmetry analysis may contain near-zaro numbers
    that result from floating point error. this component is responsible
    for cleaning up the expresion.
    '''


    def __init__(self, epsilon=1e-8):
        self.epsilon = epsilon
        import math
        self.math = math
        return
    

    def render(self, expression):
        if self.isNumber(expression): return self.onNumber(expression)
        return self.dispatch(expression)


    def isNumber(self, candidate):
        return isinstance(candidate, int) or \
               isinstance(candidate, float)


    def dispatch(self, expression):
        name = 'on'+expression.__class__.__name__.capitalize()
        if not hasattr(self, name): return expression
        method = getattr(self, name)
        return method(expression)


    def onList(self, l):
        return [self.render(e) for e in l]


    def onNumber(self, number):
        for i in range(3):
            if abs(abs(number) - i) < self.epsilon:
                return self.math.copysign(i, number)
        return number
    onReal = onNumber


    def onAdd(self, expression):
        right, left = expression.as_two_terms()
        left = self.render(left)
        right = self.render(right)
        return left+right


    def onMul(self, expression):
        right, left = expression.as_two_terms()
        left = self.render(left)
        right = self.render(right)
        try:
            return left*right
        except:
            return right*left
exp_cleaner = SympyExpressionCleaner()

# version
__id__ = "$Id$"

# End of file 
