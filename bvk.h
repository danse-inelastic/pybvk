#ifndef BVK_H
#define BVK_H

// Units: T(K), kappa(1/m)
// Performance: takes about 0.5s per 1M qs
// See Squires 3.74, with 'd' there is 'site' here
double bvkDebyeWaller(System* system,QPoint* q,EigenValue* v,EigenVector* e,
                      int nq,int site,double T,Vector* kappa);

// Computes the average Wd over the sphere of radius kappa by uniformly
// sampling the sphere with nPhi bins in the angle down from z (latitude, goes
// 0..Pi) and nTheta bins in in the angle around the circle (longitude, goes
// 0..2Pi).  Note that Griffiths uses theta and phi in the opposite sense.
double bvkDebyeWallerSphereAverage(System* system,QPoint* q,EigenValue* v,
                                   EigenVector* e,int nq,int site,double T,
                                   double kappa,int nPhi,int nTheta);

void bvkDebyeWallerPlot(System* system,QPoint* q,EigenValue* v,
                        EigenVector* e,int nq,int site,double T,
                        int nPhi,int nTheta,char* fn);

int bvkCompute(System* system,int nq,QPoint* qs,
               EigenValue** pws,EigenVector** pes);

int* bvkComputeDOS(int nq,QPoint* qs,int nSites,EigenValue* vs,double scale,
                   double wres,int* nBins,double* wMin);

double bvkMaxOmega(int nw,EigenValue* ws,double* minOmega);

#endif // BVK_H
