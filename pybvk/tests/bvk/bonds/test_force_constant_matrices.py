# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

def test():
    from bvk.bonds.force_constant_matrices import load
    load("SnTe/FORCE_CONSTANTS.txt")
    return


def main():
    test()
    return


if __name__ == '__main__': main()
