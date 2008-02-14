#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

int main(int argc,char *argv[]) {
  int N = atoi(argv[1]);

  setvbuf(stdout,NULL,_IONBF,0);
  srand48(getpid()*234597574378);

  System* system=systemRead("system");

  int nq;
  QPoint* qs=qpointGenRegularInRCell(system,&nq,N);
  printf("%d Q points\n",nq);

  qpointWrite("WeightedQ",nq,qs);

  printf("Ssee program? iss kap\\\"ut.\n");
}
