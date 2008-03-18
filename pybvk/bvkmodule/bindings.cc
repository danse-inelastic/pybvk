// -*- C++ -*-
// 
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *  
 *  Mike McKerns
 *  mmckerns@caltech.edu
 *  (C) 2008 All Rights Reserved
 *  
 *  <LicenseText>
 *  
 *~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 */
#include <portinfo>
#include <Python.h>

#include "bindings.h"
#include "misc.h"          // miscellaneous methods

// the method table
struct PyMethodDef pybvk_methods[] = {
  // sanity checking
  {pybvk_hello__name__,pybvk_hello,METH_VARARGS,pybvk_hello__doc__},
  {pybvk_copyright__name__,pybvk_copyright,METH_VARARGS,pybvk_copyright__doc__},

  // core routines

  {0, 0} // Sentinel
};

// version
// $Id$
// End of file
