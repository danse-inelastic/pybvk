#ifndef DINAW_H
#define DINAW_H

#ifdef __amd64__
  #include <acml.h>
#else
  #include "mylapack.h"
#endif // __amd64__

typedef struct {
  int n;
  doublecomplex* e;
} DynamicalMatrix;  // "Dynamical" is not a word.

static inline void dynamicalMatrixCopy(DynamicalMatrix* d,DynamicalMatrix* m) {
  // XXX: assert d.n==m.n
  memcpy(d->e,m->e,sizeof(doublecomplex)*d->n*d->n);
}

static inline void dynamicalMatrixZero(DynamicalMatrix* d) {
  memset(d->e,0,sizeof(doublecomplex)*d->n*d->n);
}

static inline void dynamicalMatrixAllocate(DynamicalMatrix* d,int n) {
  d->n=n;
  d->e=(doublecomplex*)malloc(sizeof(doublecomplex)*n*n);
  dynamicalMatrixZero(d);
}

static inline doublecomplex* dynamicalMatrixGet(DynamicalMatrix* d,int r,int c) {
  return d->e+(d->n*r)+c;
}

static inline void dynamicalMatrixSet(DynamicalMatrix* d,int r,int c,double re,
                               double im) {
  doublecomplex* v=d->e+(d->n*r)+c;
  v->real=re;
  v->imag=im;
}

static inline void dynamicalMatrixAcc(DynamicalMatrix* d,int r,int c,double re,
                               double im) {
  doublecomplex* v=d->e+(d->n*r)+c;
  v->real+=re;
  v->imag+=im;
}

static inline void dynamicalMatrixAccumulate(DynamicalMatrix* d,int fromSite,
                                      int toSite,Matrix* mRe,Matrix* mIm) {
  if(toSite<fromSite) { printf("toSite < fromSite -- lower tri"); abort(); }
  dynamicalMatrixAcc(d,fromSite*3+0,toSite*3+0,mRe->a,mIm->a);
    dynamicalMatrixAcc(d,fromSite*3+0,toSite*3+1,mRe->b,mIm->b);
      dynamicalMatrixAcc(d,fromSite*3+0,toSite*3+2,mRe->c,mIm->c);
  dynamicalMatrixAcc(d,fromSite*3+1,toSite*3+0,mRe->d,mIm->d);
    dynamicalMatrixAcc(d,fromSite*3+1,toSite*3+1,mRe->e,mIm->e);
      dynamicalMatrixAcc(d,fromSite*3+1,toSite*3+2,mRe->f,mIm->f);
  dynamicalMatrixAcc(d,fromSite*3+2,toSite*3+0,mRe->g,mIm->g);
    dynamicalMatrixAcc(d,fromSite*3+2,toSite*3+1,mRe->h,mIm->h);
      dynamicalMatrixAcc(d,fromSite*3+2,toSite*3+2,mRe->i,mIm->i);
}

static inline void dynamicalMatrixDump(DynamicalMatrix* d) {
  printf("---DynamicalMatrix:\n");
  for(int r=0;r<d->n;r++) {
    for(int c=0;c<d->n;c++) {
      char re[512],im[512];
      sprintf(re,"%9.2le",dynamicalMatrixGet(d,r,c)->real);
      if(dynamicalMatrixGet(d,r,c)->real<1e-100 &&
         dynamicalMatrixGet(d,r,c)->real>-1e-100) sprintf(re,"~0");
      sprintf(im,"%9.2le",dynamicalMatrixGet(d,r,c)->imag);
      if(dynamicalMatrixGet(d,r,c)->imag<1e-100 &&
         dynamicalMatrixGet(d,r,c)->imag>-1e-100) sprintf(im,"~0");
      printf("%9s/%-9s  ",re,im);
    }
    printf("\n");
  }
}

#endif // DINAW_H
