#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

const double dosScale=1.0/(2*M_PI*1e12); // THz
const double dBin=0.05;

int main() {
  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  System* system=systemRead("system");
  systemComputeBonds(system);

  int nq;
  QPoint* qs=qpointRead("WeightedQ",&nq); qs=qs; // Kill the warning.
  printf("%d Q points\n",nq);

  EigenVector* pols = eigenvectorRead("Polarizations");
  EigenValue* om2s = eigenvalueRead("Omega2");

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
      val+=dBin/2.0;
      for(int s=0;s<nSites;s++){
        index = nSites*dim*nSites*q + nSites*sd + s;
        weight = EigenVectorMag2(&pols[index]);
//        assert(val>0,"value must be >0");
//        int bin=(int)(val/dBin);  // bin 0 has values [0..dBin)
//                                  // bin N has values [N*dBin..(N+1)*dBin)
        int bin=(int)(val/dBin); // bin2 0 has values [-0.5*dBin..0.5*dBin)
        bins[ nBins*s + bin ] += weight;
        sums[s] += weight;
      }
    }
  }

  for(int s=0;s<nSites;s++){ for(int b=0;b<nBins;b++){
      bins[nBins*s + b] /= sums[s]*dBin;
  }}

  printf("number of bins  = %d\n",nBins);
  printf("number of sites = %d\n",nSites);
  for(int s=0;s<nSites;s++){ 
    char filename[8]; 
    sprintf(filename,"DOS.%d",s);
    int io=open(filename,O_TRUNC|O_CREAT|O_WRONLY,0644);
    char title[64] = "DOS";
    int version = 1;
    char comment[1024] = "DOS from a BvK simulation.";
    write(io,&title,sizeof(title));
    write(io,&version,sizeof(version));
    write(io,&comment,sizeof(comment));
    write(io,&nBins,sizeof(nBins));
    write(io,&dBin,sizeof(dBin));
    write(io,&bins[s*nBins],nBins*sizeof(double));
    close(io);
  }

  printf("Ssee program? iss kap\\\"ut.\n");
}
