#include <sys/time.h>
#include <stdio.h>
#include <values.h>
#include <math.h>
#include "system.h"
#include "state.h"
#include "vector.h"

#ifdef __amd64__
  #include <acml.h>
#else
  #include "mylapack.h"
  #define fastsincos sincos
  #define fastcos cos
  #define fastexp exp
#endif // __amd64__

extern void fastsincos(double t,double* sin,double* cos);
extern double fastcos(double t);
extern double fastexp(double x);

static const double hbar=1.0545716e-34;                     // kg*m^2
static const double kB=1.3806503e-23;                       // kg*m^2

// Units: T(K), kappa(1/m)
// Performance: takes about 0.5s per 1M qs
// See Squires 3.74, with 'd' there is 'site' here
double bvkDebyeWaller(System* system,QPoint* q,EigenValue* v,
                      EigenVector* e,int nq,int site,double T,Vector* kappa) {
  double W=0;

  e+=site;  // Advance to the site's polarization vector within 1st eigenvector

  // XXX: Note This ||^2 to 1 and any one of the 3 eigenvalues sum to 1/3

  // i counts throuhg all the qpoints, and for each of those,
  // j counts through all the (eigenvalue,eigenvector) pairs for this q
  // at each, e points to the length-3 (complex) polarization vector within
  // that eigenvector

  for(int i=0;i<nq;i++,q++)
    for(int j=0;j<3*system->c->sites;j++,v++,e+=system->c->sites) {
      double w=sqrt(v->v);

      double mdsR=kappa->x*e->x.real+kappa->y*e->y.real+kappa->z*e->z.real;
      double mdsI=kappa->x*e->x.imag+kappa->y*e->y.imag+kappa->z*e->z.imag;
      double magDotSq=mdsR*mdsR+mdsI*mdsI;

      // coth(x) = [exp(x)+exp(-x)] / [exp(x)-exp(-x)]
      double cotharg=hbar*w/(2*kB*T);
      double exppcotharg=fastexp(cotharg);
      double expmcotharg=1.0/exppcotharg;
      double coth=(exppcotharg+expmcotharg)/(exppcotharg-expmcotharg);

      W+=(magDotSq/w)*coth;
    }
  return W*hbar/(4*nq*system->atoms[system->sites[site].atomType].mass);
}

// Computes the average Wd over the sphere of radius kappa by uniformly
// sampling the sphere with nPhi bins in the angle down from z (latitude, goes
// 0..Pi) and nTheta bins in in the angle around the circle (longitude, goes
// 0..2Pi).  Note that Griffiths uses theta and phi in the opposite sense.
double bvkDebyeWallerSphereAverage(System* system,QPoint* q,EigenValue* v,
                                   EigenVector* e,int nq,int site,double T,
                                   double kappa,int nPhi,int nTheta) {
  double W=0;
  for(int iTheta=0;iTheta<nTheta;iTheta++) {
    for(int iPhi=0;iPhi<nPhi;iPhi++) {

      // Find the point on the sphere
      double theta=(2*M_PI*(0.5+iTheta))/nTheta;
      double phi=(M_PI*(0.5+iPhi))/nPhi;   // must be in 'bin center' for area

      // Take r,theta,phi to x,y,z
      double ct,st,cp,sp;
      fastsincos(theta,&st,&ct);
      fastsincos(phi,&sp,&cp);
      Vector k={kappa*ct*sp,kappa*st*sp,kappa*cp};

      // This is the area of the (non-differential) patch on the surface of
      // the sphere at (theta,phi), as a fraction of the total surface area
      // of the sphere.
      double thisArea=(fastcos(phi-0.5*(M_PI/nPhi))-
                       fastcos(phi+0.5*(M_PI/nPhi)))/(2*nTheta);

      W+=thisArea*bvkDebyeWaller(system,q,v,e,nq,site,T,&k);
    }
  }
  return W;
}

void bvkDebyeWallerPlot(System* system,QPoint* q,EigenValue* v,
                        EigenVector* e,int nq,int site,double T,
                        int nPhi,int nTheta,char* fn) {
  FILE* f=fopen(fn,"w");
  for(int iTheta=0;iTheta<nTheta;iTheta++) {
    for(int iPhi=0;iPhi<nPhi;iPhi++) {

      // Find the point on the sphere
      double theta=(2*M_PI*(0.5+iTheta))/nTheta;
      double phi=(M_PI*(0.5+iPhi))/nPhi;   // must be in 'bin center' for area

      // Take r,theta,phi to x,y,z
      double ct,st,cp,sp;
      fastsincos(theta,&st,&ct);
      fastsincos(phi,&sp,&cp);
      Vector k={ct*sp,st*sp,cp};   // |kappa|=1

      fprintf(f,"%le %le %le\n",theta,phi,
             bvkDebyeWaller(system,q,v,e,nq,site,T,&k));
    }
    fprintf(f,"\n");
    fprintf(stderr,".");
  }
  fclose(f);
}

static const int eigenvectorsStdout=0;

double bvkMaxOmega(int nw,EigenValue* ws,double* minOmega) {
  // Find the bounds of omega and clip to 0
  double wmax=-DBL_MAX,wmin=DBL_MAX;
  {
    EigenValue* w=ws;
    for(int i=0;i<nw;i++,w++) {
      if(w->v>wmax) wmax=w->v;
      if(w->v<wmin) wmin=w->v;
    }
  }
  if(wmin<0) {
    fprintf(stderr,"POO: wmin <0 -- negative eigenvalues not allowed\n");
    abort();
  }
  wmax=sqrt(wmax);
  wmin=sqrt(wmin);
  printf("Omega = [ %le .. %le ]\n",wmin,wmax);
  if(minOmega) *minOmega=wmin;
  return wmax;
}

int* bvkComputeDOS(int nq,QPoint* qs,int nSites,EigenValue* vs,
                   double scale,double wres,int* nBins,double* wMin) {
//outputs bin centers
  double wmin;
  double wmax=bvkMaxOmega(nq*nSites*3,vs,&wmin);
  wmax*=scale;
  int nbins=ceil(wmax/wres) + 2;
  wmin = 0.0;
  wmax = nbins*wres;
  int* bin=(int*)malloc(nbins*sizeof(int));
  memset(bin,0,nbins*sizeof(int));
  EigenValue* v=vs;
  QPoint* q=qs;
  for(int i=0;i<nq;i++,q++)
    for(int j=0;j<3*nSites;j++,v++) {
      double w=sqrt(v->v)*scale;
      int binnum=round( w/wres );
      bin[binnum]+=q->weight;
    }
  printf("DOS [%le,%le] res %le -> %d bins\n",wmin,wmax,wres,nbins);
  *wMin=wmin;
  *nBins=nbins;
  return bin;
}

int bvkCompute(System* system,int nq,QPoint* qs,
               EigenValue** pws,EigenVector** pes) {

  DynamicalMatrix d;
  dynamicalMatrixAllocate(&d,3*system->c->sites);

  struct timeval start;
  gettimeofday(&start,NULL);

  EigenValue *eigValues,*eigValue;
  *pws=eigValue=eigValues=(EigenValue*)malloc(sizeof(EigenValue)*nq*d.n);
  EigenVector *eigVectors=NULL,*eigVector=NULL;
  if(pes) *pes=eigVector=eigVectors=
    (EigenVector*)malloc(sizeof(EigenVector)*nq*d.n*d.n);

  Bond* bonds=system->bonds;

  int progress=0;
  for(int qnum=0;qnum<nq;qnum++) {
    if(progress++%10000==0) printf(".");
    QPoint* q=qs+qnum;
    dynamicalMatrixCopy(&d,&system->selfForcesD);

    for(int b=0;b<system->nBonds;b++) {
      Bond* bond=bonds+b;

      // Accumulate D_sa_sb
      double dot=q->v.x*bond->v.x+q->v.y*bond->v.y+q->v.z*bond->v.z;
      double cosWeight,sinWeight;
      fastsincos(dot,&sinWeight,&cosWeight);
      cosWeight*=bond->sqrtmfromSqrtmtoInvNeg;
      sinWeight*=bond->sqrtmfromSqrtmtoInvNeg;

      // From this base, the 9 we care about are +0+1+2, +d->n/+0+1+2,
      // +2d->n...
      doublecomplex* base=d.e+(3*d.n*bond->siteFrom)+3*bond->siteTo;
      for(int r=0;r<3;r++,base+=d.n) for(int c=0;c<3;c++) {
        (base+c)->real+=*((&(bond->rotatedFct.a))+3*r+c)*cosWeight;
        (base+c)->imag+=*((&(bond->rotatedFct.a))+3*r+c)*sinWeight;
      }
    }

    double v[d.n];
    memset(&v,0,sizeof(double)*d.n);
    int info=-1;
    // Fill array in C order in upper triangle and call with 'L' and it works
    #ifdef __amd64__
      zheev(pes?'V':'N','L',d.n,d.e,d.n,v,&info);
    #else
      char bb = 'N';
      if(pes) { bb = 'V';}
      char cc = 'L';
      int dn = d.n;
      int lwork = 2*d.n;
      //doublecomplex* work[lwork];
      doublecomplex* work;
      work = (doublecomplex *)malloc( lwork* sizeof( doublecomplex ) );
      //double rwork[lwork];
      double *rwork;
      rwork = (double *)malloc( lwork* sizeof( double ) );
      zheev(&bb,&cc,&dn,d.e,&dn,v,&work[0],&lwork,&rwork[0],&info); //FIXME
      free( work ); free( rwork );
    #endif // __amd64__
    if(info!=0) { printf("zheev failed\n"); abort(); }

    // Save the eigenvalues and eigenvectors in eig for later writing
    for(int i=0;i<d.n;i++) {
      (eigValue++)->v=v[i];
      if(pes) {
        memcpy(eigVector,&d.e[d.n*i],sizeof(doublecomplex)*d.n);
        eigVector+=d.n/3;
//        memcpy(eigVector+=d.n,&d.e[d.n*i],sizeof(doublecomplex)*d.n);
      }
    }

    if(pes && eigenvectorsStdout) {
      // Write the eivenvalues and eigenvectors to stdout
      for(int i=0;i<d.n;i++) {
        printf("%le ",v[i]);
        for(int j=0;j<d.n;j++)
          printf("%7.4lf/%7.4lf ",d.e[d.n*i+j].real,d.e[d.n*i+j].imag);
            printf("\n");
      }
    }

  }

  struct timeval finish;
  gettimeofday(&finish,NULL);

  long us=finish.tv_usec-start.tv_usec+
          (finish.tv_sec-start.tv_sec)*1000000;
  printf("\n%d q in %ld us: %ld q/s\n",nq,us,(long)(1000000.0*nq/us));

  return nq*d.n;
}
