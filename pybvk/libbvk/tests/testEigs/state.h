#ifndef STATE_H
#define STATE_H

#include <acml.h>

typedef struct {
  Vector v;
  double weight;
} QPoint;

static inline QPoint* qpointRead(char* fn,int* pnq) {
  int nq;
  QPoint* qs=NULL;
  {
    int io=open(fn,O_RDONLY);
    read(io,&nq,sizeof(nq));
    if(nq==0) {
      fprintf(stderr,"ERROR: qs file says zero qs?\n");
      abort();
    }
    qs=(QPoint*)malloc(sizeof(QPoint)*nq);
    int ntr=sizeof(QPoint)*nq;
    if(read(io,qs,ntr)!=ntr) {
      fprintf(stderr,"Read qs incomplete\n");
      abort();
    }
    close(io);
  }
  fprintf(stderr,"QPoints: %d pts\n",nq);
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

static inline EigenValue* eigenvalueRead(char* fn,int n) {
  EigenValue* eigValues=(EigenValue*)malloc(sizeof(EigenValue)*n);
  {
    int io=open(fn,O_RDONLY);
    int ntr=sizeof(double)*n;
    if(read(io,eigValues,ntr)!=ntr) {
      fprintf(stderr,"Read eigvals incomplete\n");
      abort();
    }
    close(io);
  }
  fprintf(stderr,"Eigenvalues: %d vals\n",n);
  return eigValues;
}

static inline EigenVector* eigenvectorRead(char* fn,int vlen,int nv) {
  long btr=sizeof(doublecomplex)*vlen*(vlen*nv);
  EigenVector* eigVectors=(EigenVector*)malloc(btr);
  int io=open(fn,O_RDONLY);
  if(io<0) {
    fprintf(stderr,"ERROR: Can't open %s",fn);
    perror("");
    abort();
  }
  long r=read(io,eigVectors,btr);
  if(r!=btr) {
    fprintf(stderr,"ERROR: Read eigvecs incomplete: %ld of %ld\n",r,btr);
    perror("Crap");
    abort();
  }
  close(io);
  fprintf(stderr,"Eigenvectors: %d vecs each length %d\n",vlen*nv,vlen);
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
  write(io,&nq,sizeof(nq));
  write(io,qs,nq*sizeof(QPoint));
  close(io);
}

static inline void eigenvalueWrite(char* fn,int nv,EigenValue* vs) {
  int io=open(fn,O_TRUNC|O_CREAT|O_WRONLY,0644);
//  write(io,&nv,sizeof(nv));  // XXX: Add these
  write(io,vs,nv*sizeof(EigenValue));
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
  write(io,es,sizeof(EigenVector)*nq*3*nSites*nSites);
  close(io);
}

#endif // STATE_H
