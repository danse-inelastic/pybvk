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

inline void vectorScaleAndAccumulate(Vector* r,Vector* v,double s)
  { r->x+=s*v->x; r->y+=s*v->y; r->z+=s*v->z; }

typedef struct {
  Vector v;
  double weight;
} QPoint;

int main() {
  setvbuf(stdout,NULL,_IONBF,0);

//============================================================================
//  EXAMPLE VECTORS...
//----------------------------------------------------------------------
// FOR HCP Crystals...
//----------------------------------------------------------------------
//  double A= 1.0/sqrt(3.0);
//  double B= A;        B=B;
//  double C= A/(5.616/3.577); C=C; //Holumium
//  double S=2*M_PI/sqrt(3);   S=S;
//  Vector AAA={   0, 0, 0 };
//  Vector AAA={ S*A, 0, 0 };
//  Vector AAA={ S*A, S*B/sqrt(3), 0 };
//  Vector AAA={ 0, 0, M_PI*C };
//  Vector AAA={ S*A, 0, 0 };
//  Vector AAA={ S*A, 0, M_PI*C };
//  Vector AAA={ S*A, S*B/sqrt(3), M_PI*C };
//  Vector beg={ S*A, S*B/sqrt(3), 0 };
//  Vector end={ S*A, S*B/sqrt(3), M_PI*C };
//----------------------------------------------------------------------
// FOR FCT Crystals...
//----------------------------------------------------------------------
//  Vector AAA={ 0, 0, 0 };
//  Vector AAA={ M_PI, 0, 0 };
//  Vector AAA={ M_PI, M_PI, 0 };
//  Vector AAA={ 0,0, M_PI*(4.58/4.94) };
//  Vector AAA={ M_PI,0, M_PI*(4.58/4.94) };
//============================================================================
//  USER INPUT:  start vector, end vector, number of Qs
//----------------------------------------------------------------------
  Vector beg={ 0, 0, 0 };
  Vector end={ M_PI, 0, 0 };
  int nnn=10000;
//============================================================================

  Vector dq ={ end.x-beg.x, end.y-beg.y, end.z-beg.z };
    //---------------------------------------------
    // XXX: q = q0 + t*(qf-q0) = beg + (nt/nq)*dq
    //---------------------------------------------
  int nq=0;
  QPoint* qs=(QPoint*)malloc((nnn+1)*sizeof(QPoint));
  QPoint* qc=qs;
  for(int nt=0;nt<=nnn;nt++){
    double t=(double)nt/nnn;
    memcpy(&qc->v,&beg,sizeof(beg));
    vectorScaleAndAccumulate(&qc->v,&dq,t);
    qc->weight=1;
    qc++;
    nq++;
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
