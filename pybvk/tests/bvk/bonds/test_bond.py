# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

from bvk.bonds.bond import identicalBond, uniqueBonds
from bvk.bonds.poscar import load


def test1():
    structure = load("SnTe/POSCAR.txt", 225)
    assert identicalBond((0,1), (1,2), structure)
    assert identicalBond((0,1), (1,3), structure)
    assert not identicalBond((0,1), (0,4), structure)
    assert identicalBond((4,5), (5,4), structure)
    assert identicalBond((4,5), (5,6), structure)
    assert not identicalBond((0,1), (4,5), structure)
    return


def test2():
    structure = load("SnTe/POSCAR.txt", 225)
    l = uniqueBonds(structure)
    print l
    return


def test3():
    structure = load("SnTe/SPOSCAR.txt", 225)
    l = uniqueBonds(structure)
    print l
    return


def main():
    test3()
    return


if __name__ == '__main__': main()
