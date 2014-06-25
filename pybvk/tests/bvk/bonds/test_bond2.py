# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

from bvk.bonds.bond import identicalBond, uniqueBonds
from bvk.bonds.poscar import load
from matter import Structure


def main():
    orig_structure = load("SnTe/POSCAR.txt", 225)
    super_structure = load("SnTe/SPOSCAR.txt", 225)
    structure = Structure(
        atoms=super_structure, 
        lattice=orig_structure.lattice,
        sgid = 225,
        )
    l = uniqueBonds(structure)
    print l
    return


if __name__ == '__main__': main()
