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
        workdir = 'fe_295-workdir'
        
        import os
        if os.path.exists(workdir):
            import shutil
            shutil.rmtree(workdir)
        os.makedirs(workdir)
            
        from bvk.bvkmodels import converttobvkmodelobject, fe_295
        model = converttobvkmodelobject.module2model(fe_295)
        
        from bvk import systemFromModel
        systemFromModel(model, filename=os.path.join(workdir, 'system'))
        
        cmd = 'cd %s && bvkdisp.py -d 0.1 -N 80' % workdir
        if (os.system(cmd)):
            raise RuntimeError, '%s failed' % cmd
        return        


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
