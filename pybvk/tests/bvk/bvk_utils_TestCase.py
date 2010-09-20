#!/usr/bin/env python
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


skip = True


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        from bvk.bvkmodels import converttobvkmodelobject, ce_295, fe_295

        model = converttobvkmodelobject.module2model(ce_295)
        from bvk import systemFromModel
        systemFromModel(model, filename='ce_295')
        
        model = converttobvkmodelobject.module2model(fe_295)
        from bvk import systemFromModel
        systemFromModel(model, filename='fe_295')
        return


    def test2(self):
        #computeDOS('pb_80')
        #computeDOS('fe_295')
        computeDOS('ce_295')
        return


    def test_findEquivalentSite(self):
        from bvk._utils import findEquivalentSite
        import matter
        atom1 = matter.Atom('C', [0,0,0])
        atom2 = matter.Atom('H', [0.5,0.5,0])
        atom3 = matter.Atom('H', [0.5,0,0.5])
        atom4 = matter.Atom('H', [0,0.5,0.5])

        sites = [atom2, atom3, atom4]

        from matter.SpaceGroups import sg221
        
        self.assertEqual(findEquivalentSite(atom1, sites, sg221), None)
        self.assertEqual(findEquivalentSite(atom2, sites[1:], sg221), atom3)
        self.assertEqual(findEquivalentSite(atom4, sites[:-1], sg221), atom2)
        return


    def test_findUnequivalentSites(self):
        from bvk._utils import findUnequivalentSites

        import matter
        atom1 = matter.Atom('C', [0,0,0])
        atom2 = matter.Atom('H', [0.5,0.5,0])
        atom3 = matter.Atom('H', [0.5,0,0.5])
        atom4 = matter.Atom('H', [0,0.5,0.5])
        atoms = [atom1, atom2, atom3, atom4]

        lattice = matter.Lattice(a=1,b=1,c=1,alpha=90,beta=90,gamma=90)

        struct = matter.Structure(atoms=atoms, lattice=lattice, sgid=221)

        sites, map = findUnequivalentSites(struct, struct.sg)
        self.assertEqual(len(sites), 2)
        return
    

    def test_findUniqueSpecies(self):
        from bvk._utils import findUniqueSpecies

        import matter
        atom1 = matter.Atom('C')
        atom2 = matter.Atom('H')
        atom3 = matter.Atom('H')
        atom4 = matter.Atom('H')
        atoms = [atom1, atom2, atom3, atom4]

        species, map = findUniqueSpecies(atoms)
        print species, map
        self.assertEqual(len(species), 2)
        return
        


def computeDOS(modelname, df=0.1, N=40):
    import tempfile
    workdir = tempfile.mkdtemp()

    import os
    #os.makedirs(workdir)

    from bvk.bvkmodels import converttobvkmodelobject
    exec 'from bvk.bvkmodels import %s as module' % modelname
    model = converttobvkmodelobject.module2model(module)

    from bvk import systemFromModel
    systemFromModel(model, filename=os.path.join(workdir, 'system'))
    
    cmd = 'cd %s && bvkdos.py -d %s -N %s' % (workdir, df, N)
    if (os.system(cmd)):
        raise RuntimeError, '%s failed' % cmd

    path = os.path.join(workdir, 'DOS')
    from idf.DOS import read
    info, e, I = read(path)
    import pylab;  pylab.plot(e,I); pylab.show()
    
    return workdir


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
