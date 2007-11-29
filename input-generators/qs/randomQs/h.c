#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <math.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>

//
//   //NOW OBSOLETE  qs ->
//   //NOW OBSOLETE    int32 numberOfQs
//   //NOW OBSOLETE    numberOfQs repetitions of {
//   //NOW OBSOLETE      double x,y,z
//   //NOW OBSOLETE      double weight
//   //NOW OBSOLETE    } qs
//
//   weights ->
//     int32 wedgeType -- one of:
//       0 -- wedge is monatomic-cubic irreducible wedge:
//              f0.x + nx*df.x  for nx=0..N.x-1
//                f0.y + ny*df.y  for ny=nx..N.y-1
//                  f0.z + nz*df.z  for nz=ny..N.z-1
//            where { f0.x + nx*df.x } for nx=-(N.x-1)..(N.x-1) should evenly
//            divide (periodic) -PI..PI.
//            That is, df.x*(N.x)-2*PI == df.x*-(N.x-1)
//     Vector f0 (double,double,double)
//     Vector df (double,double,double)
//     Vector N (int,int,int)
//     double weight0
//     double weight1
//     ...

#define DIE(c,m) if(c) { perror(m); abort(); }

typedef struct {
  double x,y,z;
} Vector;

inline double vectorDot(Vector* a,Vector* b) { return a->x*b->x+a->y*b->y+a->z*b
->z; }

inline void vectorCrossAndScale(Vector* r,Vector* a,Vector* b,double s) {
  r->x = s*(a->y*b->z-a->z*b->y);
  r->y = s*(a->z*b->x-a->x*b->z);
  r->z = s*(a->x*b->y-a->y*b->x);
}

typedef struct {
  Vector v;
  double weight;
} QPoint;

typedef struct {
  Vector a,b,c;
} Cell;

inline double cellVolume(Cell* a) {
  Vector tmp;
  vectorCrossAndScale(&tmp,&a->b,&a->c,1.0);
  return fabs( vectorDot(&a->a,&tmp) );
}

inline void cellReciprocal(Cell* r, Cell* a) {
  double V = 2*M_PI/cellVolume(a);
  vectorCrossAndScale(&r->a,&a->b,&a->c,V);
  vectorCrossAndScale(&r->b,&a->c,&a->a,V);
  vectorCrossAndScale(&r->c,&a->a,&a->b,V);
}

int main() {
  setvbuf(stdout,NULL,_IONBF,0);

//============================================================================
//  USER INPUT:  primitive unit cell...
//------------------------------------------------------
  double a=sqrt(3); 
  double c=(5.616/3.577)*a;
  Cell cell;
  cell.a.x=3*a/2.0;  cell.a.y=-a/2.0;  cell.a.z=0.0;
  cell.b.x=0.0;      cell.b.y=a;       cell.b.z=0.0;
  cell.c.x=0.0;      cell.c.y=0.0;     cell.c.z=c;
  Cell rCell;
//------------------------------------------------------
//  USER INPUT:  cube root of number of Q
//------------------------------------------------------
  int nnn=100;
//============================================================================

  cellReciprocal(&rCell,&cell);
  int nq=nnn*nnn*nnn;
  QPoint* qs=(QPoint*)malloc(nq*sizeof(QPoint));
  QPoint* qc=qs;
  for(int x=0;x<nnn;x++)
    for(int y=0;y<nnn;y++)
      for(int z=0;z<nnn;z++) {
        double a=drand48();
        double b=drand48();
        double c=drand48();
        qc->v.x=rCell.a.x*a+rCell.b.x*b+rCell.c.x*c;
        qc->v.y=rCell.a.y*a+rCell.b.y*b+rCell.c.y*c;
        qc->v.z=rCell.a.z*a+rCell.b.z*b+rCell.c.z*c;
//        qc->v.x=(a-0.5)*1000000000;
//        qc->v.y=(b-0.5)*1000000000;
//        qc->v.z=(c-0.5)*1000000000;
        qc->weight=1;
        qc++;
      }

  printf("%d Q points\n",nq);

  {
    int io=open("qs",O_TRUNC|O_CREAT|O_WRONLY,0644);
    write(io,&nq,sizeof(nq));
    write(io,qs,sizeof(QPoint)*nq);
    close(io);
  }

  printf("Ssee program? iss kap\\\"ut.\n");
}
