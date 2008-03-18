#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

int main(int argc,char *argv[]) {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  int withVecs=atoi(argv[1]);
  double dBin=atof(argv[2]);

  System* system=systemRead("system");
  int nSites=system->c->sites;

  int nq=0;
  QPoint* qs=qpointRead("WeightedQ",&nq);
  EigenValue* om2s = eigenvalueRead("Omega2",&nq); // Should this affect nq?
  printf("%d Q points\n",nq);

  double* bins;
  double* total;

  int nBins=0;
  if(withVecs == 1){
    EigenVector* pols; pols=0; // Kill the warning.
    pols = eigenvectorRead("Polarizations");
    nBins=pdCompute(nSites,nq,qs,om2s,pols,1,dBin,&bins,&total);
  } else { // Don't use eigenvectors
    nBins=pdCompute(nSites,nq,qs,om2s,NULL,0,dBin,&bins,&total);
  }

  printf("number of bins  = %d\n",nBins);
  printf("number of sites = %d\n",nSites);
  char filename[8]; 
  char filetype[64] = "DOS";
  int version = 1;

  if(withVecs == 1){
    char pcomment[1024] = "partial DOS from a BvK simulation.";
    for(int s=0;s<nSites;s++){ 
      sprintf(filename,"DOS.%d",s);
      dosWrite(filename,filetype,version,pcomment,nBins,dBin,&bins[s*nBins]);
    }
  }

  char tcomment[1024] = "total DOS from a BvK simulation.";
  dosWrite("DOS",filetype,version,tcomment,nBins,dBin,total);

  printf("Ssee program? iss kap\\\"ut.\n");
}
