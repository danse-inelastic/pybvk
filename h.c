#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

int main(int argc,char *argv[]) {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  System* system=systemRead("system");
  systemComputeBonds(system);

  int nq;
  QPoint* qs=qpointRead("WeightedQ",&nq);
  printf("%d Q points\n",nq);

  EigenValue* vs;

  int nv=0;
  if(atoi(argv[1]) == 1){ 
    printf("You want vectors!\n");
    EigenVector* es; 
    nv=bvkCompute(system,nq,qs,&vs,&es);
    eigenvectorWrite("Polarizations",nq,system->c->sites,es);
  }
  else{ nv=bvkCompute(system,nq,qs,&vs,NULL); }

  qpointWrite("WeightedQ",nq,qs);
  eigenvalueWrite("Omega2",nq,system->c->sites,vs);

  printf("Ssee program? iss kap\\\"ut.\n");
}
