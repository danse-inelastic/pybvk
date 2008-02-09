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
  QPoint* qs=qpointRead("WeightedQ",&nq);
  printf("%d Q points\n",nq);

  EigenVector* pols = eigenvectorRead("Polarizations");
  EigenValue* om2s = eigenvalueRead("Omega2");

  int nSites=system->c->sites;
  int dim=3;

  for(int q=0;q<nq;q++){
    for(int sd=0;sd<nSites*dim;sd++){
      for(int s=0;s<nSites;s++){

      // Check acml docs for useful doublecomplex functionality.

      }
    }
  }

  printf("Ssee program? iss kap\\\"ut.\n");
}
