#ifndef FWD_H
#define FWD_H

/*
// headers
int getDOS1(int withVecs,int N,double dBin);
int getDOS2(System* system,int type,int withVecs,int N,double dBin);
double* getDOS3(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins);
double* getDOS4(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins,int* nmq,QPoint** qps,
                EigenValue** vs,EigenVector** es);
*/

// fwd1: go from system to DOS, using file intermediates
static inline
int getDOS1(int withVecs,int N,double dBin) {
  initSetup();
  //randomQs(N);
  regularQs(N);
  h(withVecs);
  pd(withVecs,dBin);
  return 1;
}

// fwd2: system to DOS, without file intermediates
static inline
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
static inline
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
static inline
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

#endif // FWD_H
