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
    cell, atoms, sites, bonds, symRs = _systemFromModel(model)
    print cell
    print atoms
    print sites
    print bonds
    # output
    if stream is None:
        stream = open(filename, 'w')
    _write(cell, atoms, sites, bonds, symRs, stream)
    return


def _systemFromModel(model):
    matter = model.matter
    lattice = matter.lattice

    # cell
    uses_primitive_unitcell = model.uses_primitive_unitcell
    if uses_primitive_unitcell:
        cell = matter.primitive_unitcell.base.copy()
    else:
        cell = lattice.base.copy()
    cell.shape = -1
    cell = list(cell)

    # species
    if uses_primitive_unitcell:
        iteratoms = matter.primitive_unitcell.atoms
    else:
        iteratoms = matter
    species,atom2specie  = findUniqueSpecies(iteratoms)
    # Max's convention: species are called atoms
    atoms = []
    for specie in species:
        symbol = specie.symbol
        mass = specie.mass * atomic_mass_unit
        atoms.append([symbol, mass])
        continue

    # sites
    sites = []
    if uses_primitive_unitcell:
        cartesian = matter.primitive_unitcell.cartesian
    else:
        cartesian = matter.lattice.cartesian
    #
    for atom in iteratoms:
        x,y,z = cartesian(atom.xyz)
        specie = atom2specie[atom]
        i = species.index(specie)
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
        # vector from A to B. sites[i] is x,y,z, i
        va2b = np.array(sites[B][:3]) - sites[A][:3]
        Boffset = bond.Boffset
        if bond.Boffset_is_fractional:
            Boffset = cartesian(Boffset)
        vector = va2b + Boffset
        #
        #
        m = np.array(bond.force_constant_matrix)
        m.shape = -1
        #
        bonds.append([sites[A][3], sites[B][3]] + list(vector) + list(m))
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
    return cell, atoms, sites, bonds, symRs



def findUniqueSpecies(atoms):
    '''find the unique species in the given list of atoms'''    
    species = []
    map = {}
    for atom in atoms:

        # find equivalent specie in the existing specie list
        specie1 = findSpecie(atom, species)

        # if found, establishing the mapping and done
        if specie1:
            map[atom] = specie1
            continue

        # if not found, this is a new specie
        species.append(atom)
        map[atom] = atom
        
        continue
        
    return species, map



def findSpecie(atom, species):
    '''find the specie of atom in the list of species. if not found, return None'''
    for specie in species:
        if specie.symbol != atom.symbol: continue
        if specie.mass != atom.mass: continue
        return specie
    return


def findUnequivalentSites(atoms, sg):
    '''find unequivalent sites in a structure
    '''
    sites = []
    map = {}
    for atom in atoms:

        # find equivalent site in the existing site list
        site1 = findEquivalentSite(atom, sites, sg)

        # if found, establishing the mapping and done
        if site1:
            map[atom] = site1
            continue

        # if not found, this is a new site
        sites.append(atom)
        map[atom] = atom
        
        continue
        
    return sites, map



def findEquivalentSite(atom, sites, spacegroup, epsilon=1e-7):
    import numpy as np
    for site in sites:
        if atom.symbol != site.symbol:
            continue
        for symop in spacegroup.symop_list:
            transformed = symop(atom.xyz)
            diff = transformed - site.xyz
            if (np.abs(diff)<epsilon).all(): return site
            continue
        continue
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


# version
__id__ = "$Id$"

# End of file 
