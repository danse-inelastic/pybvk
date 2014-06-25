# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

import numpy as np


def uniqueBonds(structure):
    n = len(structure)
    r = []
    for i in range(n):
        for j in range(n):
            p = (i,j)
            print "examinng: %s" % (p,)
            unique = True
            for p2 in r:
                if identicalBond(p, p2, structure):
                    unique = False
                    break
                continue
            if unique:
                r.append(p)
            continue
        continue
    return r
                    

def identicalBond(pair1, pair2, structure):
    # this method checks trivial things
    # hard work is in identicalBondAB
    len1 = bondLength(pair1, structure)
    len2 = bondLength(pair2, structure)
    if not almostEqual(len1, len2): return False
    # AA or AB?
    elements1 = elements(pair1, structure)
    elements2 = elements(pair2, structure)
    if elements1[0] == elements1[1]:
        if elements2[0] != elements2[1] or elements2[0]!=elements1[0]:
            return False
        return identicalBondAB(pair1, pair2, structure) \
            or identicalBondAB(pair1, reverse(pair2), structure)
    if elements1[0] == elements2[0] and \
            elements1[1] == elements2[1]:
        return identicalBondAB(pair1, pair2, structure)
    elif elements1[0] == elements2[1] and \
            elements1[1] == elements2[0]:
        return identicalBondAB(pair1, reverse(pair2), structure)
    return False


def identicalBondAB(pair1, pair2, structure):
    for symop in structure.sg.iter_symops():
        a1, a2 = pair1
        x1 = symop(structure[a1].xyz)
        x2 = symop(structure[a2].xyz)
        b1, b2 = pair2
        x1b = structure[b1].xyz
        x2b = structure[b2].xyz
        dis = (x1b-x1) - (x2b-x2)
        if almostEqual(np.linalg.norm(dis), 0):
            return True
        continue
    return False


def reverse(l):
    l1 = list(l); l1.reverse()
    return l1


epsilon = 1e-7
def almostEqual(x1, x2):
    return abs(x1-x2) < epsilon


def elements(pair, structure):
    a,b = pair
    return structure[a].symbol, structure[b].symbol


def bondLength(pair, structure):
    a,b = pair
    pa = cartesian(a, structure)
    pb = cartesian(b, structure)
    return np.linalg.norm(pa-pb)


def cartesian(index, structure):
    atom = structure[index]
    return structure.lattice.cartesian(atom.xyz)

