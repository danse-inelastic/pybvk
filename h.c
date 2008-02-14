#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

const double dosScale=1.0/(2*M_PI*1e12);
const double dosRes=0.01;

int main(int argc,char *argv[]) {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  System* system=systemRead("system");
  systemComputeBonds(system);

  int nq;
//  QPoint* qs=qpointGenRegularInRCell(system,&nq,30);
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

//  eigenfreqWrite("freqs",nv,vs,dosScale);
//  int nBins;
//  double wMin;
//  int* dos =
//       bvkComputeDOS(nq,qs,system->c->sites,vs,dosScale,dosRes,&nBins,&wMin);
//  dosWrite("dos",nBins,dos,wMin,dosRes);

  printf("Ssee program? iss kap\\\"ut.\n");
}
