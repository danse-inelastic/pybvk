#!/usr/bin/env python
# Jiao Lin <linjiao@caltech.edu>


def test():
    from bvk.bonds.poscar import load
    load("SnTe/POSCAR.txt", 225)
    return

def main():
    test()
    return


if __name__ == '__main__': main()
