#!/usr/bin/env python
# Jiao Lin <linjiao@caltech.edu>


def test():
    from bvk.bonds.poscar import load
    structure = load("POSCAR-test-out-of-box-atom", 225)
    oob = structure[-1]
    print oob
    assert oob.xyz[0] == 1.5
    return

def main():
    test()
    return


if __name__ == '__main__': main()
