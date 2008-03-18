#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

// main: get DOSs
// assume "system" and "qpoints" generated
// assume eigenvalues and eigenvectors generated
int main(int argc,char *argv[]) {
  int withVecs=atoi(argv[1]);
  double dBin=atof(argv[2]);
  initSetup();
  pd(withVecs,dBin);
  printf("Ssee program? iss kap\\\"ut.\n");
}
