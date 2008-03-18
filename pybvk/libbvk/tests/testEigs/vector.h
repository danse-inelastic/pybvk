#ifndef VECTOR_H
#define VECTOR_H

#include <math.h>

static const double TOL=1e-8;

//-- Vector -------------------------------------------------------------------

typedef struct {
  double x,y,z;
} Vector;

static inline double vectorLength(Vector* v)
  { return sqrt(v->x*v->x+v->y*v->y+v->z*v->z); }
static inline void vectorDump(Vector* v) 
  { printf("[% 7.4lf, % 7.4lf, % 7.4lf]",v->x,v->y,v->z); }
static inline void vectorDump2stderr(Vector* v) 
  { fprintf(stderr,"[% 7.4lf, % 7.4lf, % 7.4lf]",v->x,v->y,v->z); }
static inline void vectorScaleAndAccumulate(Vector* r,Vector* v,double s)
  { r->x+=s*v->x; r->y+=s*v->y; r->z+=s*v->z; }
static inline int vectorSame(Vector* a,Vector* b) {
  // We want effectively to test if they're the same within tolerance.  Naive:
  //   return a->x-b->x<TOL && a->x-b->x>-TOL &&
  //          a->y-b->y<TOL && a->y-b->y>-TOL &&
  //          a->z-b->z<TOL && a->z-b->z>-TOL;
  // But we can do it branch-free if we sqaure things:
  double dx=a->x-b->x,dy=a->y-b->y,dz=a->z-b->z;
  return dx*dx+dy*dy+dz*dz<TOL;      // Rigorously, something like <3*TOL*TOL
}
static inline double vectorDot(Vector* a,Vector* b)
  { return a->x*b->x+a->y*b->y+a->z*b->z; }
static inline void vectorCrossAndScale(Vector* r,Vector* a,Vector* b,double s) {
  r->x = s*(a->y*b->z-a->z*b->y);
  r->y = s*(a->z*b->x-a->x*b->z);
  r->z = s*(a->x*b->y-a->y*b->x);
}
static inline void vectorNormalize(Vector* v) {
  double m=vectorLength(v);
  v->x*=m; v->y*=m; v->z*=m;
}

//-- Matrix -------------------------------------------------------------------

typedef struct {
  double a,b,c,d,e,f,g,h,i;
} Matrix;

static inline void mvMultiply(Vector* r,Matrix* m,Vector* v) {
  r->x= m->a*v->x + m->b*v->y + m->c*v->z;
  r->y= m->d*v->x + m->e*v->y + m->f*v->z;
  r->z= m->g*v->x + m->h*v->y + m->i*v->z;
}
static inline double matrixDeterminant(Matrix* m) {
  return  m->a*m->e*m->i + m->b*m->f*m->g + m->c*m->d*m->h - \
          m->a*m->f*m->h - m->b*m->d*m->i - m->c*m->e*m->g;
}
static inline void matrixInverse(Matrix* r, Matrix* m) {
  double detI = 1.0/matrixDeterminant(m);
  r->a= ( m->e*m->i-m->f*m->h )*detI;
  r->b= ( m->c*m->h-m->b*m->i )*detI;
  r->c= ( m->b*m->f-m->c*m->e )*detI;
  r->d= ( m->f*m->g-m->d*m->i )*detI;
  r->e= ( m->a*m->i-m->c*m->g )*detI;
  r->f= ( m->c*m->d-m->a*m->f )*detI;
  r->g= ( m->d*m->h-m->e*m->g )*detI;
  r->h= ( m->b*m->g-m->a*m->h )*detI;
  r->i= ( m->a*m->e-m->b*m->d )*detI;
}
static inline void matrixTranspose(Matrix* r, Matrix* m) {
  r->a=m->a; r->b=m->d; r->c=m->g;
  r->d=m->b; r->e=m->e; r->f=m->h;
  r->g=m->c; r->h=m->f; r->i=m->i;
}
static inline void matrixMultiply(Matrix* r, Matrix* a,Matrix* b) {
  r->a= a->a*b->a + a->b*b->d + a->c*b->g;
    r->b= a->a*b->b + a->b*b->e + a->c*b->h;
      r->c= a->a*b->c + a->b*b->f + a->c*b->i;
  r->d= a->d*b->a + a->e*b->d + a->f*b->g;
    r->e= a->d*b->b + a->e*b->e + a->f*b->h;
      r->f= a->d*b->c + a->e*b->f + a->f*b->i;
  r->g= a->g*b->a + a->h*b->d + a->i*b->g;
    r->h= a->g*b->b + a->h*b->e + a->i*b->h;
      r->i= a->g*b->c + a->h*b->f + a->i*b->i;
}
static inline void matrixScale(Matrix* r,Matrix* m,double s) {
  r->a=m->a*s; r->b=m->b*s; r->c=m->c*s;
  r->d=m->d*s; r->e=m->e*s; r->f=m->f*s;
  r->g=m->g*s; r->h=m->h*s; r->i=m->i*s;
}
static inline void matrixDump(Matrix* m) {
  printf("---Matrix:\n[");
  vectorDump((Vector*)&m->a); printf(",\n ");
  vectorDump((Vector*)&m->d); printf(",\n ");
  vectorDump((Vector*)&m->g); printf("]\n");
}
static inline void matrixDump2stderr(Matrix* m) {
  fprintf(stderr,"---Matrix:\n[");
  vectorDump2stderr((Vector*)&m->a); fprintf(stderr,",\n ");
  vectorDump2stderr((Vector*)&m->d); fprintf(stderr,",\n ");
  vectorDump2stderr((Vector*)&m->g); fprintf(stderr,"]\n");
}

#endif
