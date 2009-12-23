# -*- Python -*-
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


import numpy as np
atomic_mass_unit = 1.660538782e-27 # unit kg


def systemFromModel(model, stream=None, filename=None):
    '''create "system" from a bvk model data object

    model.matter is an instance of matter.Structure
    '''
    matter = model.matter
    lattice = matter.lattice

    # cell
    uses_primitive_unitcell = model.uses_primitive_unitcell
    if uses_primitive_unitcell:
        cell = matter.primitive_unitcell.base.copy()
    else:
        cell = lattice.base.copy()
    cell.shape = -1

    # atoms
    if uses_primitive_unitcell:
        iteratoms = matter.primitive_unitcell.atoms
    else:
        iteratoms = matter
    atoms = []
    for atom in iteratoms:
        symbol = atom.symbol
        mass = atom.mass * atomic_mass_unit
        atoms.append([symbol, mass])
        continue

    # sites
    sites = []
    if uses_primitive_unitcell:
        cartesian = matter.primitive_unitcell.cartesian
    else:
        cartesian = matter.lattice.cartesian
    #
    for i, atom in enumerate(iteratoms):
        x,y,z = cartesian(atom.xyz)
        sites.append([x,y,z, i])
        continue

    # bonds
    bondobjs = model.bonds
    def len2(v):
        return np.sum(np.square(v))
    def cmpbondlength(bond1, bond2):
        return int(len2(bond1.getBondVectorInCartesianCoords())-len2(bond2.getBondVectorInCartesianCoords()))
    bondobjs.sort(cmpbondlength)
    bonds = []
    for bond in bondobjs:
        #
        assert bond.uses_primitive_unitcell == uses_primitive_unitcell
        #
        A = bond.A; B = bond.B
        #
        Boffset = bond.Boffset
        if bond.Boffset_is_fractional:
            Boffset = cartesian(Boffset)
        #
        m = np.array(bond.force_constant_matrix)
        m.shape = -1
        #
        bonds.append([A, B] + list(Boffset) + list(m))
        continue

    # symRs
    symRs = getUniqueRotations(matter.sg)
    # convert to cartesian
    # the rotation matrices are in the fractional coordinates of
    # the lattice
    base = matter.lattice.base
    binv = np.linalg.inv(base)
    def toCartesian(R):
        return np.dot(np.dot(binv, R), base)
    symRs = map(toCartesian, symRs)
    # output
    if stream is None:
        stream = open(filename, 'w')

    _write(cell, atoms, sites, bonds, symRs, stream)
    return


def _write(cell, atoms, sites, bonds, symRs, stream):
    from bvk.input_generators.system.System import fatAll

    a,s,b = fatAll(atoms,sites,bonds)
    NS = len(symRs)
    stream.write( pack('=4i',len(a),len(s),len(bonds),NS ) )
    stream.write( pack('=9d',*cell) )
    for i in a:
        stream.write( pack('=64sd',*i) )
        continue
    for i in sites:
        stream.write( pack('=3d2i',*(i+(0,)) ) )
        continue
    for i in bonds:
        stream.write( pack('=2i3d9d',*i) )
        continue
    stream.write( packRotationMatricees(symRs) )
    stream.close()
    return




def writeSpaceGroupSyms(sg, f):
    '''write rotations in a space group into a file using pack
    '''
    Rs = getUniqueRotations(sg)
    packed = packRotationMatricees(Rs)

    stream = open(f, 'w')
    stream.write(pack('=i', len(Rs)))
    stream.write(packed)
    return


def getUniqueRotations(sg):
    '''find out the unique rotations in a space group
    
    sg: an instance of matter.SpaceGroups.SpaceGroup
    '''
    Rs = []; ids = []
    for o in sg.iter_symops():
        R = o.R
        if id(R) in ids: continue
        Rs.append(R); ids.append(id(R))
        continue
    return Rs


from struct import pack, unpack, calcsize
def packRotationMatricees(matrices):
    '''pack rotation matrices using struct.pack

    double*9*n  numbers
    n: number of matrices
    '''
    t = ()
    for m in matrices:
        m.shape = -1,
        t+=tuple(m)
        continue
    return pack('=%sd' % (9*len(matrices)), *t)


def writeSymsFile(matrices, f):
    '''create a symmetries file
    
    int32 number of matrices
    double*9*n  n matrices.
    '''
    stream = open(f, 'w')
    stream.write(pack('=i', len(matrices)))
    for m in matrices:
        m.shape = -1,
        stream.write( pack('=9d', *tuple(m)))
        continue
    return



import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        from bvkmodels import converttobvkmodelobject, ce_295
        model = converttobvkmodelobject.module2model(ce_295)
        systemFromModel(model, filename='ce_295')
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
