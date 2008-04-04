#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "system.h"
#include "state.h"

// main: get selected EigenVectors & EigenValues
// assume "eigenvalues" & "eigenvectors" generated
int main(int argc,char *argv[]) {
  char filename[]="Omega2";
  if(argc>1) {
    strcpy(filename,argv[1]);
  }
  int N = -1;
  if(argc>2) {
    N = atoi(argv[2]);
  }
  int withVecs=0;
  if(argc>3) {
    withVecs=atoi(argv[3]);  // use eigenvectors? (True == 1)
  }
  char filename2[]="Polarizations";
  if(argc>4) {
    strcpy(filename2,argv[4]);
  }
  int nSites = 1;
  if(argc>5) {
    nSites = atoi(argv[5]);
  }
  int dimen = 3;

  int nq;
  EigenValue* val=eigenvalueRead(filename,&nq);
  EigenVector* vec=NULL;
  if(withVecs == 1) {
    vec=eigenvectorRead(filename2);
  }
  printf("%d Q points\n",nq);

  if(N == -1) {
    for(int qp=0;qp<nq*nSites*dimen;qp++) {
      eigenPrint(val,vec,dimen,nSites,nq,qp);
    } 
  } else {
    eigenPrint(val,vec,dimen,nSites,nq,N);
  }
  printf("Ssee program? iss kap\\\"ut.\n");
}

