#!/usr/bin/env python
# Jiao Lin <linjiao@caltech.edu>


def test():
    from bvk.bonds.poscar import load
    structure = load("SnTe/POSCAR.txt", 225)
    for symop in structure.sg.iter_symops():
        print symop.R, symop.t
    return

def main():
    test()
    return


if __name__ == '__main__': main()
