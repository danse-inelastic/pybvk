#!/usr/bin/env python
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Mike McKerns
# mmckerns@caltech.edu
# (C) 2008 All Rights Reserved
# 
# <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

if __name__ == "__main__":

    import bvk
    from bvk import _bvk as bvkmodule

    print "copyright information:"
    print "   ", bvk.copyright()
    print "   ", bvkmodule.copyright()

    print
    print "module information:"
    print "    file:", bvkmodule.__file__
    print "    doc:", bvkmodule.__doc__
    print "    contents:", dir(bvkmodule)

    print
    print bvkmodule.hello()

# version
__id__ = "$Id$"
#  End of file 
