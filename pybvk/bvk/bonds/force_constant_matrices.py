# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

def load(path):
    """
    return: m[atom1, atom2, :, :] is 3X3 matrix
    """
    stream = open(path)
    line0 = stream.readline()
    natoms = int(line0)
    import numpy as np
    m = np.zeros((natoms, natoms, 3, 3), dtype='float')
    for lineno, line in enumerate(stream):
        if lineno%4 == 0:
            i,j = map(int, line.split())
            continue
        y = lineno % 4 - 1
        m[i-1,j-1,y,:] = map(float, line.split())
        continue
    return m


def test():
    load("LiChen/FORCE_CONSTANTS.txt")
    return


def main():
    test()
    return


if __name__ == '__main__': main()
