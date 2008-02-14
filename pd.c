#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

const double dosScale=1.0/(2*M_PI*1e12); // THz

int main(int argc,char *argv[]) {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  int withVecs=atoi(argv[1]);
  double dBin=atof(argv[2]);

  System* system=systemRead("system");

  int nq=0;
  EigenValue* om2s = eigenvalueRead("Omega2",&nq);
  printf("%d Q points\n",nq);

  EigenVector* pols; pols=0; // Kill the warning.
  if(withVecs == 1){
    pols = eigenvectorRead("Polarizations");
  }

  int nSites=system->c->sites;
  int dim=3;

  double maxFreq=0;
  for(int f=0;f<nq*nSites*dim;f++){
   om2s[f].v = sqrt(om2s[f].v)*dosScale;
   if( om2s[f].v > maxFreq ){ maxFreq = om2s[f].v; }
  }

  double* sums=(double*)malloc(sizeof(double)*nSites);
  for(int i=0;i<nSites;i++){ sums[i] = 0.0; }

  int nBins=(int)(maxFreq/dBin)+10;
  double* bins=(double*)malloc(sizeof(double)*nBins*nSites);
  printf("Maximum frequency = %f\n",maxFreq);

  double weight=0;
  double val=0;
  int index=0;
  for(int q=0;q<nq;q++){
    for(int sd=0;sd<nSites*dim;sd++){
      val=om2s[nSites*dim*q+sd].v;
      // assert(val>0,"value must be >0");
      val+=dBin/2.0;
      for(int s=0;s<nSites;s++){
        index = nSites*dim*nSites*q + nSites*sd + s;
        weight = 1.0;
        if(withVecs == 1){
          weight = EigenVectorMag2(&pols[index]);
        }
        int bin=(int)(val/dBin); // bin 0 has values [-0.5*dBin..0.5*dBin)
        bins[ nBins*s + bin ] += weight;
        sums[s] += weight;
      }
    }
  }

  double* total=(double*)malloc(sizeof(double)*nBins);
  for(int s=0;s<nSites;s++){ for(int b=0;b<nBins;b++){
      bins[nBins*s + b] /= sums[s]*dBin;
      total[b] += bins[nBins*s + b]/(double)nSites;
  }}

  printf("number of bins  = %d\n",nBins);
  printf("number of sites = %d\n",nSites);
  char filename[8]; 
  char filetype[64] = "DOS";
  int version = 1;

  if(withVecs == 1){
    char pcomment[1024] = "partial DOS from a BvK simulation.";
    for(int s=0;s<nSites;s++){ 
      sprintf(filename,"DOS.%d",s);
      dosWrite(filename,filetype,version,pcomment,nBins,dBin,&bins[s*nBins]);
    }
  }

  char tcomment[1024] = "total DOS from a BvK simulation.";
  dosWrite("DOS",filetype,version,tcomment,nBins,dBin,total);

  printf("Ssee program? iss kap\\\"ut.\n");
}
