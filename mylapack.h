#ifndef __MYLAPACK_H__
#define __MYLAPACK_H__

//#define myzheev zheev

typedef int integer;
typedef double doublereal;
typedef struct { doublereal r, i; } doublecomplex;

#ifdef __cplusplus
extern "C" {
#endif

int zheev( char *jobz, char *uplo, integer *n,
        doublecomplex *a, integer *lda, doublecomplex *w, doublecomplex* work,
        integer *lwork, doublereal *rwork, integer *info);


#ifdef __cplusplus
}
#endif

#endif
