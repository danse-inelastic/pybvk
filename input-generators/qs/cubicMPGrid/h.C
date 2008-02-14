#ifndef CUBICMPGRID
#define CUBICMPGRID

#include <stdio.h>
#include <vector>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include "Vector3.H"

int main(int argc,char *argv[]){
  int N  = atoi(argv[1]); 
  N -= 1;
  int start = 1;
  if(N%2 == 0){ start -= 1; }
  std::vector<Vector3> Q;
  std::vector<int> w;
  for(int i=start;i<=N;i+=2) for(int j=i;j<=N;j+=2) for(int k=j;k<=N;k+=2){
    Q.push_back( Vector3(i,j,k) ); w.push_back(1);
  }
  for(int q=0;q<(int)Q.size();q++){ 
    int zeros  = Q[q].zeros();
    int digits = Q[q].digits();
    for( int z=0; z< 3-zeros; z++ ){ w[q] *= 2; }
    if(digits == 3){ w[q] *= 6; }
    if(digits == 2){ w[q] *= 3; }
  }
  double mul = 2.0*M_PI / 2.0 / (double)(N+1) ;


  int io=open("WeightedQ",O_CREAT|O_TRUNC|O_WRONLY,0644);
  int anInt=(int)Q.size(); 

  if(sizeof(anInt)!=4) {
    printf("sizeof(int) is wrong!\n");
    exit(2);
  }

  char title[64] = "WeightedQ";
  char comment[1024];
  sprintf(comment, "%d Qs on Monkhorst-Pack grid", anInt);
  int version = 1;
  int dimension = 3;
  write(io,&title,sizeof(title));
  write(io,&version,sizeof(version));
  write(io,&comment,sizeof(comment));
  write(io,&dimension,sizeof(dimension));
  write(io,&anInt,sizeof(anInt));
  for(int q=0;q<(int)Q.size();q++){ 
    printf("%lf %lf %lf %d\n", Q[q].x*mul,Q[q].y*mul,Q[q].z*mul,w[q]);
    double dbl;
    dbl=Q[q].x*mul; write(io,&dbl,sizeof(double));
    dbl=Q[q].y*mul; write(io,&dbl,sizeof(double));
    dbl=Q[q].z*mul; write(io,&dbl,sizeof(double));
    dbl=w[q];       write(io,&dbl,sizeof(double));
  }
  close(io);
  return 0;
}

#endif // CUBICMPGRID
