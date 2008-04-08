#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "system.h"
#include "state.h"

// main: get selected qpoints
// assume "qpoints" generated
int main(int argc,char *argv[]) {
  char filename[]="DOS";
  if(argc>1) {
    strcpy(filename,argv[1]);
  }
  int N = -1;
  if(argc>2) {
    N = atoi(argv[2]);
  }

  int nBins;
  double dE;
  double* bins=dosRead(filename,&nBins,&dE);

  if(N == -1) {
    for(int bin=0;bin<nBins;bin++) {
      dosPrint(bins,nBins,bin);
    } 
  } else {
    dosPrint(bins,nBins,N);
  }
  printf("Ssee program? iss kap\\\"ut.\n");
  return 1;
}
