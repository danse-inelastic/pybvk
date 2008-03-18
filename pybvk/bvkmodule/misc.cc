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

#include "misc.h"
#include "libbvk/sanity.h"

// copyright
char pybvk_copyright__doc__[] = "";
char pybvk_copyright__name__[] = "copyright";

static char pybvk_copyright_note[] = 
  "bvk python module: Copyright (c) 2008 Mike McKerns";

PyObject * pybvk_copyright(PyObject *, PyObject *) {
  return Py_BuildValue("s", pybvk_copyright_note);
}
    
// hello
char pybvk_hello__doc__[] = "";
char pybvk_hello__name__[] = "hello";

PyObject * pybvk_hello(PyObject *, PyObject *) {
  return Py_BuildValue("s", hello());
}
    
// version
// $Id$
// End of file
