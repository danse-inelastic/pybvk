#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

const double dosScale=1.0/(2*M_PI*1e12);
const double dosRes=0.011;

int main() {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  System* system=systemRead("system");
  systemComputeBonds(system);

  int nq;
  QPoint* qs=qpointGenRegularInRCell(system,&nq,1);
//  QPoint* qs=qpointRead("qs",&nq);
  fprintf(stderr,"%d Q points\n",nq);

  EigenValue* vs;
//  int nv=bvkCompute(system,nq,qs,&vs,NULL);
  EigenVector* es; int nv=bvkCompute(system,nq,qs,&vs,&es);

  qpointWrite("qs",nq,qs);
  eigenvalueWrite("eigval",nv,vs);
  eigenfreqWrite("freqs",nv,vs,dosScale);
  eigenvectorWrite("eigvec",nq,system->c->sites,es);

  int nBins;
  double wMin;
  int* dos=bvkComputeDOS(nq,qs,system->c->sites,vs,dosScale,dosRes,
                         &nBins,&wMin);
  dosWrite("dos",nBins,dos,wMin,dosRes);

  fprintf(stderr,"Ssee program? iss kap\\\"ut.\n");
}
