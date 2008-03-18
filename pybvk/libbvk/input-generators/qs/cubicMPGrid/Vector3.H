#ifndef VECTOR3_H
#define VECTOR3_H

#include <math.h>

class Vector3 {
  public:
    inline Vector3(void): x(0),y(0),z(0) { }
    inline Vector3(int x,int y,int z): x(x),y(y),z(z) { }
    inline int zeros(void){
      int count = 0;
      if( x == 0){ count++; }
      if( y == 0){ count++; }
      if( z == 0){ count++; }
      return count;
    }
    inline int digits(void){
      if( x == y && x == z ){ return 1; }
      if( x == y && x != z ){ return 2; }
      if( x == z && y != z ){ return 2; }
      if( z == y && x != z ){ return 2; }
      return 3;
    }
    inline void dump(void) const { printf("<%d,%d,%d>\n",x,y,z); }
  public:
    int x,y,z;
};

#endif // VECTOR3_H
