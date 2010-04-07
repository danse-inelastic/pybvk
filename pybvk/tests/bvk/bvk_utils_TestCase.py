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
        computeDOS('pb_80')
        # computeDOS('fe_295')
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
