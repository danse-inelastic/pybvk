#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"
#include "fwd.h"

// main
int main(int argc,char *argv[]) {
  int N = atoi(argv[1]);     // number Q points?
  double dBin=atof(argv[2]); // bin width?
  int withVecs=0;
  if(argc>3) {
    withVecs=atoi(argv[3]);  // use eigenvectors? (True == 1)
  }
  int type = 0; // random Qpoints
  if(argc>4) {               // Q point distribution? (select from list)
    if(strcmp(argv[4],"regular") == 0) { type = 10; } //XXX: was type=1
  }
  char sysname[]="system";
  if(argc>5) {               // name of system? (select from list)
    strcpy(sysname,argv[5]);
  }
  int useFiles=0;
  if(argc>6) {
    useFiles=atoi(argv[6]);  // write to file intermediates? (True == 1)
  }
  // getDOS1(withVecs,N,dBin);                // fwd1
  System* system = systemRead(sysname);       // fwd2, fwd3
  // getDOS2(system,type,withVecs,N,dBin);    // fwd2
  int nBins;                                  // fwd3, fwd4
  double* bins;                               // fwd3, fwd4
  //double* total = getDOS3(system,type,withVecs,N,dBin,&nBins,&bins); // fwd3
  int nq;                                     // fwd4...
  QPoint* qs=NULL;
  EigenValue* om2s=NULL;
  EigenVector* pols=NULL;
  double* total = getDOS4(system,type,withVecs,N,dBin,&nBins,&bins,
                          &nq,&qs,&om2s,&pols); // ...fwd4
  totalDosWrite(nBins,dBin,total);            // fwd3, fwd4...
  int nSites = system->c->sites;
  if(withVecs == 1) {
    partialDosWrite(nSites,nBins,dBin,bins);
  }                                           // ...fwd3, fwd4
  if(useFiles == 1) {                         // fwd4...
    qpointWrite("WeightedQ",nq,qs);
    eigenvalueWrite("Omega2",nq,nSites,om2s);
    if(withVecs == 1) {
      eigenvectorWrite("Polarizations",nq,nSites,pols);
    }
  }                                           // ...fwd4
  //printf("Ssee program? iss kap\\\"ut.\n");
  return 1;
}
