#include <stdio.h>
#include <stdlib.h>
#include "vector.h"
#include "system.h"
#include "state.h"
#include "bvk.h"

// main: generate regular q-points
int main(int argc,char *argv[]) {
  int N = atoi(argv[1]);
  int inclusive = 0;
  if (argc==3)
    inclusive = atoi(argv[2]);

  initSetup();
  int type = 10+inclusive;
  printf("regularQs: inclusive=%d\n", inclusive);
  printf("regularQs: N=%d\n", N);
  printf("regularQs: type=%d\n", type);
  Qps(type, N);
  
  printf("Ssee program? iss kap\\\"ut.\n");
}
