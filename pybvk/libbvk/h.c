#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

// main: get eigenvalues & eigenvectors
// assume "system" and "qpoints" generated
int main(int argc,char *argv[]) {
  int withVecs=atoi(argv[1]);
  initSetup();
  h(withVecs);
  printf("Ssee program? iss kap\\\"ut.\n");
}

