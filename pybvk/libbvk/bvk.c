#include <sys/time.h>
#include <stdio.h>
#include <values.h>
#include <math.h>
#include "system.h"
#include "state.h"
#include "vector.h"
#include "bvk.h"

// (un)comment the following line for debugging output
//#define debug

#ifdef __amd64__
  #include <acml.h>
  #include <acml_mv.h>
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

const double dosScale=1.0/(2*M_PI*1e12); // THz

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
    fprintf(stderr,"POO: wmin = %lf <0 -- no negative frequencies\n",wmin);
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

#ifdef debug
  int progress=0;
#endif // debug
  for(int qnum=0;qnum<nq;qnum++) {
#ifdef debug
    if(progress++%10000==0) printf(".");
#endif // debug
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
    // Fill array in C order in upper triangle and call with 'L' and it works
    #ifdef __amd64__
    int info=-1;
      zheev(pes?'V':'N','L',d.n,d.e,d.n,v,&info);
    #else
    long int info=-1;
      char bb = 'N';
      if(pes) { bb = 'V';}
      char cc = 'L';
      int dn = d.n;
      int lwork = 2*dn-1;
      // generate doublecomplex work[lwork]
      doublecomplex *work;
      work = (doublecomplex *)malloc( lwork* sizeof( doublecomplex ) );
      // generate double rwork[lwork]
      double *rwork;
      rwork = (double *)malloc( (3*dn-2)*sizeof( double ) );
      // call to zheev using 'standard' clapack interface
      zheev(&bb,&cc,&dn,d.e,&dn,v,work,&lwork,rwork,&info);
      free( work ); free( rwork );
    #endif // __amd64__
    if(info!=0) { printf("zheev failed\n"); abort(); }

    // Save the eigenvalues and eigenvectors in eig for later writing
    if(pes) { //use eigenvectors
      for(int i=0;i<d.n;i++) {
        (eigValue++)->v=v[i];
        memcpy(eigVector,&d.e[d.n*i],sizeof(doublecomplex)*d.n);
        eigVector+=d.n/3;
//      memcpy(eigVector+=d.n,&d.e[d.n*i],sizeof(doublecomplex)*d.n);
      }
      if(eigenvectorsStdout) { //Write eigenvalues & eigenvectors to stdout
        for(int i=0;i<d.n;i++) {
          printf("%le ",v[i]);
          for(int j=0;j<d.n;j++)
            printf("%7.4lf/%7.4lf ",d.e[d.n*i+j].real,d.e[d.n*i+j].imag);
              printf("\n");
        }
      }
    } else { //don't use eigenvectors
      for(int i=0;i<d.n;i++) {
      (eigValue++)->v=v[i];
      }
    }
  }

  struct timeval finish;
  gettimeofday(&finish,NULL);

#ifdef debug
  long us=finish.tv_usec-start.tv_usec+
          (finish.tv_sec-start.tv_sec)*1000000;
  printf("\n%d q in %ld us: %ld q/s\n",nq,us,(long)(1000000.0*nq/us));
#endif // debug

  return nq*d.n;
}

int pdCompute(int nSites,int nq,QPoint* qs,
              EigenValue* om2s,EigenVector* pols,
              double dBin,double** dbins,double** dtotal) {

  int dim=3;
  double maxFreq=0;
  EigenValue* ev2s=(EigenValue*)malloc(sizeof(EigenValue)*nq*dim*nSites);
#ifdef debug
  printf("ev2s=%p, size=%d\n", ev2s, sizeof(EigenValue)*nq*dim*nSites);
#endif
  
  double omega;
  for(int f=0;f<nq*nSites*dim;f++){
   omega = om2s[f].v;
   if (omega<0) {
#ifdef debug
    printf("** Warning: negative frequency. f=%d, omega=%g\n", f, omega);
#endif
    omega = 0;
   }

   ev2s[f].v = sqrt(omega)*dosScale;
   if( ev2s[f].v > maxFreq ){ maxFreq = ev2s[f].v; }
  }
#ifdef debug
  printf("Maximum frequency = %f\n",maxFreq);
#endif // debug

  int nBins=(int)(maxFreq/dBin)+10;
  double* bins=(double*)malloc(sizeof(double)*nBins*nSites);
#ifdef debug
  printf("bins size=%d, bins=%p\n", sizeof(double)*nBins*nSites, bins);
#endif
  for(int i=0;i<nSites*nBins;i++){ bins[i] = 0.0; }

  double* sums=(double*)malloc(sizeof(double)*nSites);
  for(int i=0;i<nSites;i++){ sums[i] = 0.0; }


  double weight=0;
  double val=0;
  int index=0, index1;
  if(pols) { // use eigenvectors
    for(int q=0;q<nq;q++){
      for(int sd=0;sd<nSites*dim;sd++){
        index1 = nSites*dim*q+sd;
        val=ev2s[index1].v;
        // assert(val>0,"value must be >0");
        val+=dBin/2.0;
        for(int s=0;s<nSites;s++){
          weight = qs[q].weight;
          index = nSites*dim*nSites*q + nSites*sd + s;  //XXX: withVecs
          weight *= EigenVectorMag2(&pols[index]);      //XXX: withVecs
          int bin=(int)(val/dBin); // bin 0 has values [-0.5*dBin..0.5*dBin)
#ifdef debug
#endif
          bins[ nBins*s + bin ] += weight;
          sums[s] += weight;
        }
      }
    }
  } else { //XXX: same as above, w/o the two withVecs lines
    for(int q=0;q<nq;q++){
      for(int sd=0;sd<nSites*dim;sd++){
        val=ev2s[nSites*dim*q+sd].v;
        // assert(val>0,"value must be >0");
        val+=dBin/2.0;
        for(int s=0;s<nSites;s++){
          weight = qs[q].weight;
          int bin=(int)(val/dBin); // bin 0 has values [-0.5*dBin..0.5*dBin)
          bins[ nBins*s + bin ] += weight;
          sums[s] += weight;
        }
      }
    }
  }
  free( ev2s );

  double* total=(double*)malloc(sizeof(double)*nBins);
  for(int b=0;b<nBins;b++){ total[b] = 0.0; }

  for(int s=0;s<nSites;s++){ for(int b=0;b<nBins;b++){
      bins[nBins*s + b] /= sums[s]*dBin;
      total[b] += bins[nBins*s + b]/(double)nSites;
  }}
  free( sums );

  *dbins=bins;
  *dtotal=total;
  return nBins;
}

// XXX: 'file-driven' methods ----------

// get DOSs
int pd(int withVecs,double dBin) {
  System* system=systemRead("system");
  int nSites=system->c->sites;

  int nq=0;
  QPoint* qs=qpointRead("WeightedQ",&nq);
  EigenValue* om2s = eigenvalueRead("Omega2",&nq); // Should this affect nq?
#ifdef debug
  printf("%d Q points\n",nq);
#endif // debug

  double* bins;
  double* total;

  int nBins=0;
  if(withVecs == 1){
    EigenVector* pols; pols=0; // Kill the warning.
    pols = eigenvectorRead("Polarizations");
    nBins=pdCompute(nSites,nq,qs,om2s,pols,dBin,&bins,&total);
    //XXX: total=generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);
  } else { // Don't use eigenvectors
    nBins=pdCompute(nSites,nq,qs,om2s,NULL,dBin,&bins,&total);
    //XXX: total=generateDOS(nSites,nq,qs,om2s,NULL,dBin,&nBins,&bins);
  }
#ifdef debug
  printf("number of bins  = %d\n",nBins);
  printf("number of sites = %d\n",nSites);
#endif // debug

  if(withVecs == 1){
    partialDosWrite(nSites,nBins,dBin,bins);
  }
  totalDosWrite(nBins,dBin,total);
  return 1;
}

// write partial DOSs to file
void partialDosWrite(int nSites,int nBins,double dBin,double* bins) {
  char filename[8]; 
  char filetype[64] = "DOS";
  int version = 1;
  char pcomment[1024] = "partial DOS from a BvK simulation.";
  for(int s=0;s<nSites;s++){ 
    sprintf(filename,"DOS.%d",s);
    dosWrite(filename,filetype,version,pcomment,nBins,dBin,&bins[s*nBins]);
  }
  return;
}

// write total DOS to file
void totalDosWrite(int nBins,double dBin,double* total) {
  char filetype[64] = "DOS";
  int version = 1;
  char tcomment[1024] = "total DOS from a BvK simulation.";
  dosWrite("DOS",filetype,version,tcomment,nBins,dBin,total);
  return;
}

// get eigenvalues & eigenvectors
// NOTE: reads 'system','WeightedQ' files
//       writes 'Omega2','Polarizations' files
int h(int withVecs) {
  System* system=systemRead("system");
  int nSites=system->c->sites;

  int nq;
  QPoint* qs=qpointRead("WeightedQ",&nq);
#ifdef debug
  printf("%d Q points\n",nq);
#endif // debug

  //XXX: Better to return eigenvector or eigenvalue? (see bvk.h)
  //EigenValue* vs;
  //EigenVector* es=generateEigenValues(withVecs,system,nq,qs,&vs);
  EigenVector* es=NULL;
  EigenValue* vs=generateEigenValues(withVecs,system,nq,qs,&es);
  //XXX: Better to merge "generateEigenValues" with "bvkCompute"?

  if(withVecs == 1){ 
    //printf("You want vectors!\n");
    eigenvectorWrite("Polarizations",nq,nSites,es);
  }
  qpointWrite("WeightedQ",nq,qs);
  eigenvalueWrite("Omega2",nq,nSites,vs);
  return 1;
}

// generate q-points
// NOTE: reads 'system' file
//       writes 'WeightedQ' file
int Qps(int type,int N) {
  System* system=systemRead("system");

  int nq;
  QPoint* qs=generateQpoints(type,system,&nq,N);
#ifdef debug
  printf("%d Q points\n",nq);
#endif // debug

  qpointWrite("WeightedQ",nq,qs);
  return 1;
}

// generate random q-points
int randomQs(int N) { // type = 0
  return Qps(0,N);
}

// generate regular q-points
int regularQs(int N) { // type = 1
  return Qps(10,N); //XXX: was type=1... what about type=11?
}

// XXX: targets for python bindings -----

// hide vanilla setup stuff here
int initSetup(void) {
  setvbuf(stdout,NULL,_IONBF,0);
  //srand48(getpid()*234597574378);
  srand48(getpid()*2345975743);
  return 1;
}

// generate qpoints for selected system
// NOTE: new qpoint methods go here
// NOTE: types of q points
//   10: regular Qs in the 1BZ. boundaries not included
//   11: regular Qs in the 1BZ. boundaries are included
//   0:  random Qs in the 1BZ.
QPoint* generateQpoints(int type,System* system,int* nq,int N) {
  int nqs;
  QPoint* qs;
#ifdef debug
  printf("generateQpoints: type=%d\n", type);
#endif // debug
  switch (type) {
  case 10:
    qs=qpointGenRegularInRCell(system,&nqs,N);
    break;
  case 11:
    qs=qpointGenRegularInRCell(system,&nqs,N, 1);
    break;
  case 0: 
    qs=qpointGenRandomInRCell(system,&nqs,N);
    break;
  default:
    throw;
  }
  *nq=nqs;
  return qs;
}

// generate random q-points for selected system
QPoint* generateRandomQs(System* system,int* nq,int N) {
  int nqs;
  QPoint* qs=generateQpoints(0,system,&nqs,N);
  *nq = nqs;
  return qs;
} // type = 0

// generate regular q-points for selected system
QPoint* generateRegularQs(System* system,int* nq,int N) {
  int nqs;
  QPoint* qs=generateQpoints(10,system,&nqs,N);
  *nq = nqs;
  return qs;
} // type = 1

/*
//XXX: Better to return eigenvector or eigenvalue?
// get eigenvalues & eigenvectors
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
double* generateDOS(int nSites,int nq,QPoint* qs,
                     EigenValue* om2s,EigenVector* pols,
                     double dBin,int* nmbins,double** pdbins) {
  double* bins;
  double* total;
  // NOTE: if not using eigenvectors, assume they are passed in as NULL
  int nBins=pdCompute(nSites,nq,qs,om2s,pols,dBin,&bins,&total);
#ifdef debug
  printf("number of bins  = %d\n",nBins);
  printf("number of sites = %d\n",nSites);
#endif // debug

  *nmbins = nBins;
  *pdbins = bins;
  return total;
}
