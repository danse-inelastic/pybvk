#ifndef STATE_H
#define STATE_H

#include <acml.h>

typedef struct {
  Vector v;
  double weight;
} QPoint;

static inline QPoint* qpointRead(char* fn,int* pnq) {
  int nq;
  char title[64]; 
  int version;
  char comment[1024];
  int dimension;
  QPoint* qs=NULL;
  {
    int io=open(fn,O_RDONLY);
    read(io,&title,sizeof(title));
    // if(nq==0) {
    //   printf("ERROR: WeightedQ file has no title?\n");
    //   abort();
    // }
    read(io,&version,sizeof(version));
    if(version!=1) {
      printf("ERROR: WeightedQ file is not version 1.\n");
      abort();
    }
    read(io,&comment,sizeof(comment));
    // if(nq==0) {
    //   printf("ERROR: WeightedQ file has no comment?\n");
    //   abort();
    // }
    read(io,&dimension,sizeof(dimension));
    if(dimension!=3) {
      printf("ERROR: WeightedQ file is not 3 dimensional.\n");
      abort();
    }
    read(io,&nq,sizeof(nq));
    if(nq==0) {
      printf("ERROR: WeightedQ file says zero Qs?\n");
      abort();
    }
    qs=(QPoint*)malloc(sizeof(QPoint)*nq);
    int ntr=sizeof(QPoint)*nq;
    if(read(io,qs,ntr)!=ntr) {
      printf("Read WeightedQs incomplete\n");
      abort();
    }
    close(io);
  }
  printf("QPoints: %d pts\n",nq);
  *pnq=nq;
  return qs;
}

// XXX: If you ever read qs, remember your generators might need fixing to
//      scale the q vectors by 2Pi

static inline QPoint* qpointGenRegularInRCell(System* system,int* pnq,int n) {
  *pnq=n*n*n;
  Cell* rcell=&system->rcell;
  QPoint* qs=(QPoint*)malloc(*pnq*sizeof(QPoint));
  QPoint* qc=qs;
  for(int x=0;x<n;x++)
    for(int y=0;y<n;y++)
      for(int z=0;z<n;z++) {
        double a=drand48();
        double b=drand48();
        double c=drand48();
        qc->v.x=rcell->a.x*a+rcell->b.x*b+rcell->c.x*c;
        qc->v.y=rcell->a.y*a+rcell->b.y*b+rcell->c.y*c;
        qc->v.z=rcell->a.z*a+rcell->b.z*b+rcell->c.z*c;
        qc->weight=1;
        qc++;
      }
  return qs;
}

typedef struct {
  double v;
} EigenValue;

typedef struct {
  doublecomplex x,y,z;
} EigenVector; // XXX: Should really be called PolarizationVector

static inline EigenValue* eigenvalueRead(char* fn) {
// static inline EigenValue* eigenvalueRead(char* fn,int n) {
  int nq;
  char title[64]; 
  int version;
  char comment[1024];
  int dimension;
  int nSites;
    int io=open(fn,O_RDONLY);
    read(io,&title,sizeof(title));
    // if(nq==0) {
    //   printf("ERROR: Polarizations file has no title?\n");
    //   abort();
    // }
    read(io,&version,sizeof(version));
    if(version!=1) {
      printf("ERROR: Polarizations file is not version 1.\n");
      abort();
    }
    read(io,&comment,sizeof(comment));
    // if(version!=1) {
    //   printf("ERROR: Polarizations file has no comment?\n");
    //   abort();
    // }
    read(io,&dimension,sizeof(dimension));
    if(dimension!=3) {
      printf("ERROR: Polarizations file is not of dimension 3.\n");
      abort();
    }
    read(io,&nSites,sizeof(nSites));
    // if(nSites!=3) {
    //   printf("ERROR: Polarizations file has wrong number of sites.\n");
    //   abort();
    // }
    read(io,&nq,sizeof(nq));
    // if(nq!=3) {
    //   printf("ERROR: Polarizations file has wrong number of qs.\n");
    //   abort();
    // }
  int n=nq*nSites*dimension;
  EigenValue* eigValues=(EigenValue*)malloc(sizeof(EigenValue)*n);
  {
    int ntr=sizeof(double)*n;
    if(read(io,eigValues,ntr)!=ntr) {
      printf("Read eigvals incomplete\n");
      abort();
    }
    close(io);
  }
  printf("Eigenvalues: %d vals\n",n);
  return eigValues;
}

static inline EigenVector* eigenvectorRead(char* fn) {
//static inline EigenVector* eigenvectorRead(char* fn,int vlen,int nv) {
//  long btr=sizeof(doublecomplex)*vlen*(vlen*nv);
//  EigenVector* eigVectors=(EigenVector*)malloc(btr);
  int nq;
  char title[64]; 
  int version;
  char comment[1024];
  int dimension;
  int nSites;
  int io=open(fn,O_RDONLY);
  if(io<0) {
    fprintf(stderr,"ERROR: Can't open %s",fn);
    perror("");
    abort();
  }
    read(io,&title,sizeof(title));
    // if(nq==0) {
    //   printf("ERROR: Polarizations file has no title?\n");
    //   abort();
    // }
    read(io,&version,sizeof(version));
    if(version!=1) {
      printf("ERROR: Polarizations file is not version 1.\n");
      abort();
    }
    read(io,&comment,sizeof(comment));
    // if(version!=1) {
    //   printf("ERROR: Polarizations file has no comment?\n");
    //   abort();
    // }
    read(io,&dimension,sizeof(dimension));
    if(dimension!=3) {
      printf("ERROR: Polarizations file is not of dimension 3.\n");
      abort();
    }
    read(io,&nSites,sizeof(nSites));
    // if(nSites!=3) {
    //   printf("ERROR: Polarizations file has wrong number of sites.\n");
    //   abort();
    // }
    read(io,&nq,sizeof(nq));
    // if(nq!=3) {
    //   printf("ERROR: Polarizations file has wrong number of qs.\n");
    //   abort();
    // }
  long btr=sizeof(doublecomplex)*nq*nSites*dimension*nSites*dimension;
  EigenVector* eigVectors=(EigenVector*)malloc(btr);
  long r=read(io,eigVectors,btr);
  if(r!=btr) {
    printf("ERROR: Read eigvecs incomplete: %ld of %ld\n",r,btr);
    perror("Crap");
    abort();
  }
  close(io);
  printf("Polarizations: %d vecs each length %d\n",
                                        nq*nSites*nSites*dimension,dimension);
  return eigVectors;
}

static inline void eigenvectorDumpAll(EigenValue* v,EigenVector* e,
                                      int dn,int nq) {
  // XXX: Only prints first polarization vector in the eigenvector
  for(int i=0;i<dn*nq;i++) {
    printf("%le: % le%+lei ",v->v,e->x.real,e->x.imag);
    printf("% le%+lei ",e->y.real,e->y.imag);
    printf("% le%+lei\n",e->z.real,e->z.imag);
    e+=dn/3,v++;
  }
}

static inline void dosWrite(char* fn,int nbins,int* bins,double wMin,
                            double wRes) {
  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
  for(int i=0;i<nbins;i++) {
    char buf[512];
    sprintf(buf,"%lf %lf\n",i*wRes+wMin,(double)bins[i]);
    write(io,buf,strlen(buf));
  }
  close(io);
}

static inline void qpointWrite(char* fn,int nq,QPoint* qs) {
  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
  char title[64] = "WeightedQ";
  int version = 1;
  char comment[1024] = "WeightedQ from a BvK simulation.";
  int dimension = 3;
  write(io,&title,sizeof(title));
  write(io,&version,sizeof(version));
  write(io,&comment,sizeof(comment));
  write(io,&dimension,sizeof(dimension));
  write(io,&nq,sizeof(nq));
  write(io,qs,nq*sizeof(QPoint));
  close(io);
}

static inline void eigenvalueWrite(char* fn,int nq,int nSites,EigenValue* vs) {
  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
  char title[64] = "Omega2";
  int version = 1;
  char comment[1024] = "Omega**2 from a BvK simulation.";
  int dimension = 3;
  write(io,&title,sizeof(title));
  write(io,&version,sizeof(version));
  write(io,&comment,sizeof(comment));
  write(io,&dimension,sizeof(dimension));
  write(io,&nSites,sizeof(nSites));
  write(io,&nq,sizeof(nq));
  write(io,vs,nq*nSites*3*sizeof(EigenValue));
  close(io);
}

static inline void eigenfreqWrite(char* fn,int nv,EigenValue* vs,
                                   double scale) {
  EigenValue* vc=(EigenValue*)malloc(nv*sizeof(EigenValue));
  for(int i=0;i<nv;i++) vc[i].v=sqrt(vs[i].v)*scale; // XXX: POO makes sqrt safe

  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
  write(io,&nv,sizeof(nv));  // XXX: Add these
  write(io,vc,nv*sizeof(EigenValue));
  close(io);

  free(vc);
}

static inline void eigenvectorWrite(char* fn,int nq,int nSites,
                                    EigenVector* es) {
  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
  char title[64] = "Polarizations";
  int version = 1;
  char comment[1024] = "Polarization vectors from a BvK simulation.";
  int dimension = 3;
  write(io,&title,sizeof(title));
  write(io,&version,sizeof(version));
  write(io,&comment,sizeof(comment));
  write(io,&dimension,sizeof(dimension));
  write(io,&nSites,sizeof(nSites));
  write(io,&nq,sizeof(nq));
  write(io,es,sizeof(EigenVector)*nq*3*nSites*nSites);
  close(io);
}

#endif // STATE_H
