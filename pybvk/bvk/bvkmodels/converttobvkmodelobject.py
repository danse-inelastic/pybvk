# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy


from bvk.BvKModel import BvKModel
from bvk.BvKBond import BvKBond
from matter import Lattice, Atom, Structure


# convert a module in this directory to a BvKModel data object
class ConvertModuleToModel(object):


    def __call__(self, module):
        return self._convertToModel(module)


    def _convertToModel(self, module):
        if module.lattice_type not in ['bcc', 'fcc']: return

        ltype = module.lattice_type
        handler = '_convert%sModel' % ltype
        print ' * converting %s ...' % module.__name__
        return getattr(self, handler)(module)


    def _convertbccModel(self, module):
        atom1 = Atom(module.element)
        atom2 = Atom(module.element, [0.5,0.5,0.5])
        atoms = [atom1, atom2]
        a = module.a
        lattice = Lattice(a=a,b=a,c=a, alpha=90, beta=90, gamma=90)
        description = '%s %s at %sK' % (module.lattice_type, module.element, module.temperature)
        struct = Structure(lattice=lattice, sgid=229, atoms=atoms, description=description)

        model = BvKModel()
        model.matter = struct
        model.short_description = 'bvk model of %s from literature' % description
        try:
            model.long_description = module.details
        except AttributeError:
            pass
        try:
            model.reference = module.reference
        except AttributeError:
            pass

        bonds = []
        for bond, fc in module.force_constants.iteritems():
            vec = numpy.array(map(float, bond))/2.
            bvkbond = BvKBond()
            bvkbond.matter = struct
            bvkbond.A = bvkbond.B = 0
            bvkbond.Boffset = vec
            try:
                bvkbond.force_constant_matrix = eval('bcc%s' % bond)(fc)
            except:
                import traceback
                raise RuntimeError, 'failed to convert force constant matrix. module %s, bond %s, fc %s\n%s' % (module.__name__, bond, fc, traceback.format_exc())
            bonds.append(bvkbond)
            continue

        model.bonds = bonds
        return model
    
        
    def _convertfccModel(self, module):
        atom1 = Atom(module.element)
        atom2 = Atom(module.element, [0.5,0.5,0])
        atom3 = Atom(module.element, [0.5,0,0.5])
        atom4 = Atom(module.element, [0,0.5,0.5])
        atoms = [atom1, atom2, atom3, atom4]
        a = module.a
        lattice = Lattice(a=a,b=a,c=a, alpha=90, beta=90, gamma=90)
        description = '%s %s at %s' % (module.lattice_type, module.element, module.temperature)
        struct = Structure(lattice=lattice, sgid=225, atoms=atoms, description=description)

        model = BvKModel()
        model.matter = struct
        model.short_description = 'bvk model of %s from literature' % description
        try:
            model.long_description = module.details
        except AttributeError:
            pass
        try:
            model.reference = module.reference
        except AttributeError:
            pass

        bonds = []
        for bond, fc in module.force_constants.iteritems():
            vec = numpy.array(map(float, bond))/2.
            bvkbond = BvKBond()
            bvkbond.matter = struct
            bvkbond.A = bvkbond.B = 0
            bvkbond.Boffset = vec
            try:
                bvkbond.force_constant_matrix = eval('fcc%s' % bond)(fc)
            except:
                import traceback
                raise RuntimeError, 'failed to convert force constant matrix. module %s, bond %s, fc %s\n%s' % (module.__name__, bond, fc, traceback.format_exc())
            bonds.append(bvkbond)
            continue

        model.bonds = bonds
        return model


module2model = ConvertModuleToModel()



def fcc110(fc):
    xx = fc['xx']
    xy = fc['xy']
    zz = fc['zz']
    return [[xx, xy, 0],
            [xy, xx, 0],
            [0, 0, zz]]


def fcc200(fc):
    xx = fc['xx']
    yy = fc['yy']
    return [[xx, 0, 0],
            [0, yy, 0],
            [0, 0, yy]]


def fcc211(fc):
    xx = fc['xx']
    yy = fc['yy']
    xz = fc['xz']
    yz = fc['yz']
    return [[xx, xz, xz],
            [xz, yy, yz],
            [xz, yz, yy]]


fcc220 = fcc110


def fcc310(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    xy = fc['xy']
    return [[xx, xy, 0],
            [xy, yy, 0],
            [0, 0, zz]]


def fcc222(fc):
    xx = fc['xx']
    xy = fc['xy']
    return [[xx, xy, xy],
            [xy, xx, xy],
            [xy, xy, xx]]


def fcc321(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    yz = fc['yz']
    xz = fc['xz']
    xy = fc['xy']
    return [[xx, xy, xz],
            [xy, yy, yz],
            [xz, yz, zz]]


fcc400 = fcc200




def bcc111(fc):
    xx = fc['xx']
    xy = fc['xy']
    return [[xx, xy, xy],
            [xy, xx, xy],
            [xy, xy, xx]]


def bcc200(fc):
    xx = fc['xx']
    yy = fc['yy']
    return [[xx, 0, 0],
            [0, yy, 0],
            [0, 0, yy]]


def bcc220(fc):
    xx = fc['xx']
    xy = fc['xy']
    zz = fc['zz']
    return [[xx, xy, 0],
            [xy, xx, 0],
            [0, 0, zz]]


def bcc311(fc):
    xx = fc['xx']
    yy = fc['yy']
    yz = fc['yz']
    xz = fc['xz']
    return [[xx, xz, xz],
            [xz, yy, yz],
            [xz, yz, yy]]


bcc222 = bcc111
bcc400 = bcc200

def bcc133(fc):
    xx = fc['xx']
    yy = fc['yy']
    yz = fc['yz']
    xy = fc.get('xy') or fc['xz']
    return [[xx, xy, xy],
            [xy, yy, yz],
            [xy, yz, yy]]


def bcc420(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    xy = fc['xy']
    return [[xx, xy, 0],
            [xy, yy, 0],
            [0, 0, zz]]




import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        import al_300
        module2model(al_300)
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
