#ifndef BVK_H
#define BVK_H

// Units: T(K), kappa(1/m)
// Performance: takes about 0.5s per 1M qs
// See Squires 3.74, with 'd' there is 'site' here
double bvkDebyeWaller(System* system,QPoint* q,EigenValue* v,EigenVector* e,
                      int nq,int site,double T,Vector* kappa);

// Computes the average Wd over the sphere of radius kappa by uniformly
// sampling the sphere with nPhi bins in the angle down from z (latitude, goes
// 0..Pi) and nTheta bins in in the angle around the circle (longitude, goes
// 0..2Pi).  Note that Griffiths uses theta and phi in the opposite sense.
double bvkDebyeWallerSphereAverage(System* system,QPoint* q,EigenValue* v,
                                   EigenVector* e,int nq,int site,double T,
                                   double kappa,int nPhi,int nTheta);

void bvkDebyeWallerPlot(System* system,QPoint* q,EigenValue* v,
                        EigenVector* e,int nq,int site,double T,
                        int nPhi,int nTheta,char* fn);

int bvkCompute(System* system,int nq,QPoint* qs,
               EigenValue** pws,EigenVector** pes);

int* bvkComputeDOS(int nq,QPoint* qs,int nSites,EigenValue* vs,double scale,
                   double wres,int* nBins,double* wMin);

double bvkMaxOmega(int nw,EigenValue* ws,double* minOmega);

int pdCompute(int nSites,int nq,QPoint* qs,
              EigenValue* om2s,EigenVector* pols,
              double dBin,double** dbins,double** dtotal);

int h(int withVecs);

int pd(int withVecs,double dBin);

//XXX: 'file-driven' methods ----------
void partialDosWrite(int nSites,int nBins,double dBin,double* bins);

void totalDosWrite(int nBins,double dBin,double* total);

int Qps(int type,int N);

int randomQs(int N);

int regularQs(int N);

//XXX: targets for python bindings -----
// (also see state.h)
int initSetup(void);

/*
//XXX: Better to return eigenvector or eigenvalue?
// get eigenvalues & eigenvectors
static inline
EigenVector* generateEigenValues(int withVecs,System* system,int nq,
                                 QPoint* qs,EigenValue** vs) {
  systemComputeBonds(system);
  EigenValue* vus;

  int nv=0;
  if(withVecs == 1){ 
    EigenVector* es; 
    nv=bvkCompute(system,nq,qs,&vus,&es);
    *vs = vus;
    return es;
  }
  nv=bvkCompute(system,nq,qs,&vus,NULL);
  *vs = vus;
  return NULL;
}
*/

// get eigenvalues & eigenvectors
static inline
EigenValue* generateEigenValues(int withVecs,System* system,int nq,
                                 QPoint* qs,EigenVector** es) {
  systemComputeBonds(system); //XXX: Belongs inside generateEigenValues?
  EigenValue* vs;

  int nv=0;
  if(withVecs == 1){ 
    EigenVector* evs; 
    nv=bvkCompute(system,nq,qs,&vs,&evs);
    *es = evs;
  } else {
    nv=bvkCompute(system,nq,qs,&vs,NULL);
    *es = NULL;
  }
  return vs;
}

// get DOSs
// XXX: Is this useful? ...probably better to simply adjust pdCompute
static inline
double* generateDOS(int nSites,int nq,QPoint* qs,
                     EigenValue* om2s,EigenVector* pols,
                     double dBin,int* nmbins,double** pdbins) {
  double* bins;
  double* total;
  // NOTE: if not using eigenvectors, assume they are passed in as NULL
  int nBins=pdCompute(nSites,nq,qs,om2s,pols,dBin,&bins,&total);

  *nmbins = nBins;
  *pdbins = bins;
  return total;
}

#endif // BVK_H
