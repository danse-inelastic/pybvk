#ifndef SYSTEM_H
#define SYSTEM_H

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "die.h"
#include "vector.h"
#include "dinaw.h"

// The input files:
//
//   "the cell" == the thing that's tiled to fill space, described by three
//                 vectors from (0,0,0) in cartesian world coordinates
//
//   system ->
//      int32 numberOfAtoms,numberOfSites,numberOfBonds,numberOfSymmetries
//      double c1x,c1y,c1z   +
//      double c2x,c2y,c2z   | These define the cell
//      double c3x,c3y,c3z   +
//      numerOfAtoms repetitions of {
//        char comment[64]      // Description of the atom type for reporting
//        double mass
//      } atoms                 // each repetition is a separate atom 'type'
//      numberOfSites repetitions of {
//        double x,y,z          // loc of site within the cell
//        int32 atomType        // atom type at that location
//        int32 _padding        // pad to 8-byte boundary
//      } sites 
//      numberOfBonds repetitions of {
//        int32 fromAtomType,toAtomType 
//        double x,y,z          // canonical bond vector
//        double a,b,c 
//        double d,e,f
//        double g,h,i
//      } bonds 
//      numberOfSymmetries repetitions of {  // _complete_ list of symmetries
//        double a,b,c,d,e,f,g,h,i
//      } symmetries
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

typedef struct {
  int atoms,sites,cbonds,symmetries;
} Counts;

typedef struct {
  Vector a,b,c;
} Cell;

typedef struct {
  char comment[64];
  double mass;
} Atom;

typedef struct {
  Vector v;
  int atomType;
  int _padding;
} Site;

typedef struct {
  int fromAtomType,toAtomType;
  Vector v;
  Matrix fct;
} CanonicalBond;

typedef struct {
  Matrix m;
} Symmetry;

typedef struct {
  double sqrtmfromSqrtmtoInvNeg;
  double mfromInv;
  double selfCoeff2;
  Vector v;
  Matrix rotatedFct;
  int siteFrom,siteTo;
  Vector bondExpRe,bondExpIm; // These are exp{i dq_x b_x},y,z
} Bond;

//XXX: Cell should probably be a matrix.
static inline void cellDump(Cell* c) {
  printf("---Cell:\n[");
  vectorDump(&c->a); printf(",\n ");
  vectorDump(&c->b); printf(",\n ");
  vectorDump(&c->c); printf("]\n");
}

static inline double cellVolume(Cell* a) {
  Vector tmp;
  vectorCrossAndScale(&tmp,&a->b,&a->c,1.0);
  return fabs( vectorDot(&a->a,&tmp) );
}

static inline void cellReciprocal(Cell* r, Cell* a) {
  double V = 2*M_PI/cellVolume(a);
  vectorCrossAndScale(&r->a,&a->b,&a->c,V);
  vectorCrossAndScale(&r->b,&a->c,&a->a,V);
  vectorCrossAndScale(&r->c,&a->a,&a->b,V);
}

typedef struct {
  char* buf;
  Counts* c;
  Cell* cell;
  Atom* atoms;
  Site* sites;
  CanonicalBond* cbonds;
  Symmetry* symmetries;

  // Computed stuff:
  Cell rcell;
  int nBonds;
  Bond* bonds;
  DynamicalMatrix selfForcesD;
} System;

static inline System* systemRead(char* fn) {
  System* self=(System*)malloc(sizeof(System));

  int io=open(fn,O_RDONLY); DIE(io<0,"open system");
  Counts c;
  DIE(read(io,&c,sizeof(c))!=sizeof(c),"read counts");
  int sz=sizeof(Cell)+c.atoms*sizeof(Atom)+c.sites*sizeof(Site)+
         c.cbonds*sizeof(CanonicalBond)+c.symmetries*sizeof(Symmetry);
  self->buf=(char*)malloc(sizeof(Counts)+sz);
  memcpy(self->buf,&c,sizeof(Counts));
  DIE(read(io,self->buf+sizeof(Counts),sz)!=sz,"read system");
  off_t at=lseek(io,0,SEEK_CUR);
  DIE(at!=lseek(io,0,SEEK_END),"not at eof after read system");
  close(io);
  printf("System: 1 Cell, %d Atoms, %d Sites, %d CanonicalBonds, %d "
         "Symmetries\n",c.atoms,c.sites,c.cbonds,c.symmetries);

  char* system=self->buf;
  self->c=(Counts*)system; system+=sizeof(Counts);
  self->cell=(Cell*)system;  system+=sizeof(Cell);
  self->atoms=(Atom*)system; system+=c.atoms*sizeof(Atom);
  self->sites=(Site*)system; system+=c.sites*sizeof(Site);
  self->cbonds=(CanonicalBond*)system; system+=c.cbonds*sizeof(CanonicalBond);
  self->symmetries=(Symmetry*)system;

  cellReciprocal(&self->rcell,self->cell);

  return self;
}

extern int systemComputeBonds(System* system);

#endif // SYSTEM_H
