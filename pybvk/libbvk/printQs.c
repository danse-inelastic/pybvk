#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "system.h"
#include "state.h"

// main: get selected qpoints
// assume "qpoints" generated
int main(int argc,char *argv[]) {
  char filename[]="WeightedQ";
  if(argc>1) {
    strcpy(filename,argv[1]);
  }
  int N = -1;
  if(argc>2) {
    N = atoi(argv[2]);
  }

  int nq;
  QPoint* qs=qpointRead(filename,&nq);
  printf("%d Q points\n",nq);

  if(N == -1) {
    for(int qp=0;qp<nq;qp++) {
      qpointPrint(qs,nq,qp);
    } 
  } else {
    qpointPrint(qs,nq,N);
  }
  printf("Ssee program? iss kap\\\"ut.\n");
}

