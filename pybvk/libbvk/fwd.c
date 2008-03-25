#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

//------------------------------------------
// headers
int getDOS1(int withVecs,int N,double dBin);
int getDOS2(System* system,int type,int withVecs,int N,double dBin);
double* getDOS3(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins);
double* getDOS4(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins,int* nmq,QPoint** qps,
                EigenValue** vs,EigenVector** es);
//------------------------------------------

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
    if(strcmp(argv[4],"regular") == 0) { type = 1; }
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
  printf("Ssee program? iss kap\\\"ut.\n");
  return 1;
}

// fwd1: go from system to DOS, using file intermediates
int getDOS1(int withVecs,int N,double dBin) {
  initSetup();
  //randomQs(N);
  regularQs(N);
  h(withVecs);
  pd(withVecs,dBin);
  return 1;
}

// fwd2: system to DOS, without file intermediates
int getDOS2(System* system,int type,int vec,int N,double dBin) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);

  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  // save to file
  totalDosWrite(nBins,dBin,total);
  if(vec == 1) {
    partialDosWrite(nSites,nBins,dBin,bins);
  }
  int useFiles = 0; // NOTE: allow turn on/off 'intermediate' files
  if(useFiles == 1) {
    qpointWrite("WeightedQ",nq,qs);
    eigenvalueWrite("Omega2",nq,nSites,om2s);
    if(vec == 1) {
      eigenvectorWrite("Polarizations",nq,nSites,pols);
    }
  }
  return 1;
}

// fwd3: system to DOS, without file intermediates, return DOS
double* getDOS3(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);

  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  // save to file
  int useFiles = 0; // NOTE: allow turn on/off 'intermediate' files
  if(useFiles == 1) {
    qpointWrite("WeightedQ",nq,qs);
    eigenvalueWrite("Omega2",nq,nSites,om2s);
    if(vec == 1) {
      eigenvectorWrite("Polarizations",nq,nSites,pols);
    }
  }
  *nmbins = nBins;
  *pdbins = bins;
  return total;
}

// fwd4: system to DOS, w/o file intermediates, return DOS & intermediates
double* getDOS4(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins,int* nmq,QPoint** qps,
                EigenValue** vs,EigenVector** es) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);

  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  *nmbins = nBins;
  *pdbins = bins;
  *nmq = nq;
  *qps = qs;
  *vs = om2s;
  *es = pols;
  return total;
}
