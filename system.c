#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "dinaw.h"

#ifdef __amd64__
  #include <acml.h>
#else
  #include "mylapack.h"
#endif // __amd64__

static int _computeBonds(System* system) {
  int result=0;

  // Get the arrays into convenient names
  Counts* c=system->c;
  Cell* cell=system->cell;
  Atom* atoms=system->atoms;
  Site* sites=system->sites;
  CanonicalBond* cbonds=system->cbonds;
  Symmetry* symmetries=system->symmetries;
  DynamicalMatrix* selfForces=&system->selfForcesD;
  Bond* bonds=NULL;

  if(system->nBonds) {
    // Allocate space to stash the bonds
    bonds=system->bonds=(Bond*)malloc(system->nBonds*sizeof(Bond));
    dynamicalMatrixAllocate(selfForces,3*c->sites);

    for(int n=0;n<c->sites;n++) {
      Site* site=&sites[n];
      printf("Site %d: atom %d at ",n,site->atomType);
      vectorDump(&site->v);
      printf("\n");
    }
    for(int b=0;b<c->cbonds;b++) {
      CanonicalBond* bond=&cbonds[b];
      printf("CBond: %d->%d ",bond->fromAtomType,bond->toAtomType);
      vectorDump(&bond->v); printf(" FCT:\n");
      matrixDump(&bond->fct);
    }
  }

  Matrix cellM={ cell->a.x,cell->b.x,cell->c.x,
                 cell->a.y,cell->b.y,cell->c.y,
                 cell->a.z,cell->b.z,cell->c.z };
  Matrix cellMI; matrixInverse(&cellMI,&cellM);

  for(int fromSiteN=0;fromSiteN<c->sites;fromSiteN++) {
    Site* fromSite=&sites[fromSiteN];

    for(int b=0;b<c->cbonds;b++) {
      CanonicalBond* bond=&cbonds[b];

      // We want to consider only bonds of the correct fromAtomType for the
      // current fromSite
      if(fromSite->atomType!=bond->fromAtomType) continue;

      int nextCanonicalBondTo=0;
      Vector bondTos[c->symmetries];

      for(int s=0;s<c->symmetries;s++) {
        Symmetry* symmetry=&symmetries[s];
        Vector sbondv;
        mvMultiply(&sbondv,&symmetry->m,&bond->v);

        // XXX: Note this is done before adding fromSite->v so we could maybe
        // precompute it.
        int skipThisOne=0;
        for(int bti=0;bti<nextCanonicalBondTo;bti++) {
          if(vectorSame(&bondTos[bti],&sbondv)) { skipThisOne=1; break; }
        }
        if(skipThisOne) continue;
        memcpy(&bondTos[nextCanonicalBondTo],&sbondv,sizeof(sbondv));
        nextCanonicalBondTo++;

        vectorScaleAndAccumulate(&sbondv,&fromSite->v,1.0);

        Vector image;
        mvMultiply(&image,&cellMI,&sbondv);
        // We floor here rather than trunc so it works right for negative #s
        int ia=floor(image.x+TOL);
        int ib=floor(image.y+TOL);
        int ic=floor(image.z+TOL);

        Vector sbondvdebug;
        memcpy(&sbondvdebug,&sbondv,sizeof(sbondv));

        // Shift sbondv into the cell and figure out which site is there
        // XXX: Could write this as cellM*{-ia,-ib,-ic} and accumulate that
        vectorScaleAndAccumulate(&sbondv,&cell->a,-ia);
        vectorScaleAndAccumulate(&sbondv,&cell->b,-ib);
        vectorScaleAndAccumulate(&sbondv,&cell->c,-ic);

        // Assert shifted sbondv is in the cell
        mvMultiply(&image,&cellMI,&sbondv);
        if(image.x+TOL<0 || image.x-TOL>1 ||
           image.y+TOL<0 || image.y-TOL>1 ||
           image.z+TOL<0 || image.z-TOL>1) {
          printf("CRAP! Shifted sbondv is not in cell.  In cell coords:\n");
          vectorDump(&image); printf("\n");
          abort();
        }

        // Flip through and figure out what site that location is (with tol)
        Site* toSite=NULL;
        for(int s=0;s<c->sites;s++) {
          Site* site=&sites[s];
          if(vectorSame(&site->v,&sbondv)) {
            if(toSite!=NULL) {
              printf("CRAP: image maps to more than one site!\n");
              abort();
            }
            if(site->atomType!=bond->toAtomType) {
              // Assuming there aren't two sites at the same location (that
              // would be nonsense) then if this happens, we know that we're
              // done with this symmetry*canonicalbond; it simply didn't
              // match.  toSite will still be NULL and the following block
              // will get us moved along to the next sym*sb to try.
              continue;
            }
            toSite=site;
            // Could break here (and in the atomType if), but let's keep
            // going through and make sure to puke if two sites are on the
            // same location.
          }
        }

        // If the bond we were looking at didn't hit a site, there's no
        // match.  Move on and try some more bonds.
        if(toSite==NULL) continue;

#if 0
// This isn't an error condition anymore.
          printf("CRAP: image doesn't map to a site!\n");
          printf("fromSite %d, bond %d and symmetry %d are:\n",fromSiteN,b,s);
          vectorDump(&bond->v); printf("\n");
          matrixDump(&symmetry->m);
          printf("image in cell (which is not a site) is:\n");
          vectorDump(&sbondv); printf("\n");
          printf("image in cell in cell coords is:\n");
          vectorDump(&image); printf("\n");
          printf("bond to (before shift to cell to become image) is:\n");
          vectorDump(&sbondvdebug); printf("\n");
          abort();
#endif

        // If the atom at the site this symmetric image of the bond would
        // point to is not the right atom type, then this is not the right
        // FCT for the pair of actual sites.
        if(toSite->atomType!=bond->toAtomType) continue;

        // AAA: Skip the bonds that would fill in the LOWER triangle of the
        // (Hermitian) dynamical matrix.
// XXX: This makes HCP wrong
//        if(fromSite-sites>toSite-sites) continue;

        if(bonds) {
          printf("  bond from %s ",atoms[fromSite->atomType].comment);
          vectorDump(&fromSite->v);
          printf(" to %s ",atoms[toSite->atomType].comment);
          Vector toV; memcpy(&toV,&fromSite->v,sizeof(toV));
          mvMultiply(&sbondv,&symmetry->m,&bond->v);
          vectorScaleAndAccumulate(&toV,&sbondv,1.0);
          vectorDump(&toV);
          printf("\n");

          bonds->sqrtmfromSqrtmtoInvNeg=
            -1.0/sqrt(atoms[fromSite->atomType].mass*
                      atoms[toSite->atomType].mass);
          bonds->mfromInv=1.0/atoms[fromSite->atomType].mass;
          mvMultiply(&bonds->v,&symmetry->m,&bond->v);

          Matrix m;
          matrixMultiply(&m,&symmetry->m,&bond->fct);
          Matrix t;
          matrixTranspose(&t,&symmetry->m);
          matrixMultiply(&bonds->rotatedFct,&m,&t);

          bonds->siteFrom=fromSite-sites;
          bonds->siteTo=toSite-sites;

          // Thinking in terms of the Matrix (neo):
          // We're filling the diagonal as in the full case.  Because D is
          // Hermetian, anything that goes above the (block) diagonal has to go
          // below the diagonal (conjugated).  Thus, every term above the
          // diagonal makes a contribution to the self forces for itself and
          // for its below-diagonal counterpart.
          //
          // In terms of the atoms (there's a picture in notes/atoms.jpg):
          //
          // In the first case, when both to and from atoms are within the
          // cell, we would add a self-contribution from each of those two
          // bonds.  Since one of the sites is 'less', we'd end up dropping
          // one of those bonds at AAA and have to add the other direction
          // back in.

// XXX: Probably need to drop this because it's depending on inv??? sym
//      to generate the flips of all bonds, so that anything which would
//      go lower->upper also goes upper->lower and you can drop half.
//      Really we should NOT drop this, eliminate the inv??? syms from FCC
//      and force double-expression of the bonds in the input system so that
//      the right thing happens with FCC.  ?  Or just drop the double-bonds
//      in the input file entirely -- perhaps THAT was what we were planning.

          // In the second case, where the to-atom was NOT in the cell,
          // we would NOT have added in a self-force originating at that
          // to atom.  But we _would_ have added a self-force originating
          // at the in-cell image of the to-atom and going to an _image_
          // of the from-atom (which yields the same site pair).  So in this
          // case we do the SAME thing as the first case.
          //
          // This third case is that the to atom is an image of the from
          // atom.  In this case we would NOT have included the bond for
          // the other direction in the full computation, so we don't count
          // that case (fromsite==tosite) twice.
          //
          // The 'full computation' is defined as all the bonds originating
          // at an atom in the cell -- stencilling this over all space yields
          // the full bond web (images of the cell generate the incoming bonds
          // to the cell).
          //
          // Max asserts that the FCT for the site-reversed bond equals the
          // FCT for the forward bond because -I*F*(-I)^t == F
          doublecomplex* base;

// XXX: This is to compensate for the XXX above and at AAA; we're inputting
//      the full system (all bonds originating in the cell)
#if 0
          if(bonds->siteFrom!=bonds->siteTo) {
            // Accumulate D_sa_sa onto the diagonal (the "self force")
            base=selfForces->e+(3*selfForces->n*bonds->siteTo)+3*bonds->siteTo;
            for(int r=0;r<3;r++,base+=selfForces->n) for(int c=0;c<3;c++)
              (base+c)->real+=*((&(bonds->rotatedFct.a))+r*3+c)/
                              atoms[toSite->atomType].mass;
          }
#endif

          // Accumulate D_sa_sa onto the diagonal (the "self force")
          base=selfForces->e+(3*selfForces->n*bonds->siteFrom)
                            +3*bonds->siteFrom;
          for(int r=0;r<3;r++,base+=selfForces->n) for(int c=0;c<3;c++)
            (base+c)->real+=*((&(bonds->rotatedFct.a))+r*3+c)/
                            atoms[fromSite->atomType].mass;

          bonds++;
        }

        result++;
      }
    }
  }
  return result;
}

int systemComputeBonds(System* system) {
  system->nBonds=_computeBonds(system);
  printf("There are %d bonds\n",system->nBonds);
  return _computeBonds(system);
}
