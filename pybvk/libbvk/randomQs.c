#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

// main: generate random q-points
int main(int argc,char *argv[]) {
  int N = atoi(argv[1]);
  initSetup();
  randomQs(N);
  printf("Ssee program? iss kap\\\"ut.\n");
}
