#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "system.h"

// main: get selected system
// assume "system" generated
int main(int argc,char *argv[]) {
  char filename[]="system";
  if(argc>1) {
    strcpy(filename,argv[1]);
  }
  int AT = -1; // always print all atoms
  int SI = -1; // always print all sites
  int CB = -1; // default is print all cbonds
  if(argc>2) {
    CB = atoi(argv[2]); // select cbond #
  }
  int SY = -2; // default is don't print symmetries
  if(argc>3) {
    SY = atoi(argv[3]); // select symmetry #
  }

  System* system=systemRead(filename);

  cellPrint(system);
  int atoms = system->c->atoms;
  if(AT == -1) {
    for(int atom=0;atom<atoms;atom++) {
      atomPrint(system,atom);
    } 
  } else {
    atomPrint(system,AT);
  }
  int sites = system->c->sites;
  if(SI == -1) {
    for(int site=0;site<sites;site++) {
      sitePrint(system,site);
    } 
  } else {
    sitePrint(system,SI);
  }
  int cbonds = system->c->cbonds;
  if(CB == -1) {
    for(int cbond=0;cbond<cbonds;cbond++) {
      cbondPrint(system,cbond);
    } 
  } else if(CB >= 0) {
    cbondPrint(system,CB);
  }
  int symmetries = system->c->symmetries;
  if(SY == -1) {
    for(int sym=0;sym<symmetries;sym++) {
      symPrint(system,sym);
    } 
  } else if(SY >= 0) {
    symPrint(system,SY);
  }
  printf("Ssee program? iss kap\\\"ut.\n");
  return 1;
}
