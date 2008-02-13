#ifndef __MYLAPACK_H__
#define __MYLAPACK_H__

#define zgeev_f zgeev_
#define zheev_f zheev_

typedef int integer;
typedef double doublereal;
typedef struct { doublereal r, i; } doublecomplex;

#ifdef __cplusplus
extern "C" {
#endif

int zgeev_f( char *jobvl, char *jobvr, integer *n,
        doublecomplex *a, integer *lda, doublecomplex *w, doublecomplex *vl,
        integer *ldvl, doublecomplex *vr, integer *ldvr, doublecomplex *work,
        integer *lwork, doublereal *rwork, integer *info);

int zheev_f( char *jobz, char *uplo, integer *n,
        doublecomplex *a, integer *lda, doublecomplex *w, doublecomplex* work, integer *lwork,
        doublereal *rwork, integer *info);


#ifdef __cplusplus
}
#endif

#endif
