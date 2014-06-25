# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

from matter import Atom, Lattice, Structure
import numpy as np

def load(path, sgid):
    lines = open(path).readlines()
    elements = lines[0].split()
    ne = len(elements)
    scale = float(lines[1])
    def tovector(type):
        return lambda line: map(type, line.split())
    vectors = map(tovector(float), lines[2:5])
    numbers = tovector(int)(lines[5])
    assert ne == len(numbers)
    natoms = sum(numbers)
    skip = lines[6]
    positions = map(tovector(float), lines[7:7+natoms])
    
    # lattice
    base = np.array(vectors)
    base *= scale
    lattice = Lattice(base=base)
    
    # atom list
    # compute element symbols of all atoms
    elems = []
    for n, e in zip(numbers, elements): elems += n*[e]
    # now build the atom list
    atoms = [Atom(e, xyz=pos)
             for e, pos in zip(elems, positions)]
    
    # structure
    s = Structure(atoms=atoms, lattice=lattice, sgid=sgid)
    return s


def test():
    load("LiChen/POSCAR.txt", 225)
    return

def main():
    test()
    return


if __name__ == '__main__': main()
