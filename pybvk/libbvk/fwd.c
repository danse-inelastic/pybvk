#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

//------------------------------------------
// headers
int getDOS(int withVecs,int N,double dBin);
//------------------------------------------

// main
int main(int argc,char *argv[]) {
  int withVecs=atoi(argv[1]);
  int N = atoi(argv[2]);
  double dBin=atof(argv[3]);
  getDOS(withVecs,N,dBin);
  printf("Ssee program? iss kap\\\"ut.\n");
}

// fwd1: go from system to DOS
int getDOS(int withVecs,int N,double dBin) {
  initSetup();
  //randomQs(N);
  regularQs(N);
  h(withVecs);
  pd(withVecs,dBin);
  return 1;
}
