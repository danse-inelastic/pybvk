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
#ifdef WIN32
#include "stdafx.h"
#endif

#include <portinfo>
#include <Python.h>

#include "exceptions.h"
#include "bindings.h"

// Initialization function for the module
char pybvk_module__doc__[] = "bvk forward dynamics\n";
extern "C"
#ifdef WIN32
__declspec(dllexport)
#endif
//void initbvk(void) {
void init_bvk(void) {
  PyObject *mod, *dic;
  // create the module and add the functions
  //mod = Py_InitModule4("bvk",pybvk_methods,
  mod = Py_InitModule4("_bvk",pybvk_methods,
                       pybvk_module__doc__,0,PYTHON_API_VERSION);
  // get its dictionary
  dic = PyModule_GetDict(mod);
  // check for errors
  if (PyErr_Occurred()) {
      Py_FatalError("can't initialize module bvk");
  }
  // install the module exceptions
  pybvk_runtimeError = PyErr_NewException("bvk.runtime",0,0);
  PyDict_SetItemString(dic,"RuntimeException",pybvk_runtimeError);
  return;
}

// version
// $Id$
// End of file
