#ifndef FWD_H
#define FWD_H

/*
// headers
int getDOS1(int withVecs,int N,double dBin);
int getDOS2(System* system,int type,int withVecs,int N,double dBin);
double* getDOS3(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins);
double* getDOS4(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins,int* nmq,QPoint** qps,
                EigenValue** vs,EigenVector** es);
*/

// fwd1: go from system to DOS, using file intermediates
static inline
int getDOS1(int withVecs,int N,double dBin) {
  initSetup();
  //randomQs(N);
  regularQs(N);
  h(withVecs);
  pd(withVecs,dBin);
  return 1;
}

// used to "correct" errors in DOS data... NO CLUE WHY THIS WORKS.
// DOS now only gets numerically large "spikes" when dBin is increased
// enough to push the DOS far enough to the left that the origin is
// no longer a point roughly on the DOS curve.
static inline void dirtyHACK(void) {
  System* foo=(System*)malloc(sizeof(System));
  foo = foo;
  QPoint* bar=(QPoint*)malloc(sizeof(QPoint));
  bar = bar;
  System* oof=(System*)malloc(sizeof(System));
  oof = oof;
  QPoint* rab=(QPoint*)malloc(sizeof(QPoint));
  rab = rab;
  System* fof=(System*)malloc(sizeof(System));
  fof = fof;
  QPoint* bab=(QPoint*)malloc(sizeof(QPoint));
  bab = bab;
  System* ofo=(System*)malloc(sizeof(System));
  ofo = ofo;
  QPoint* aba=(QPoint*)malloc(sizeof(QPoint));
  aba = aba;

  System* aaa=(System*)malloc(sizeof(System));
  aaa = aaa;
  QPoint* bbb=(QPoint*)malloc(sizeof(QPoint));
  bbb = bbb;
  System* ccc=(System*)malloc(sizeof(System));
  ccc = ccc;
  QPoint* ddd=(QPoint*)malloc(sizeof(QPoint));
  ddd = ddd;
  System* eee=(System*)malloc(sizeof(System));
  eee = eee;
  QPoint* fff=(QPoint*)malloc(sizeof(QPoint));
  fff = fff;
  System* ggg=(System*)malloc(sizeof(System));
  ggg = ggg;
  QPoint* hhh=(QPoint*)malloc(sizeof(QPoint));
  hhh = hhh;
  System* iii=(System*)malloc(sizeof(System));
  iii = iii;
  QPoint* jjj=(QPoint*)malloc(sizeof(QPoint));
  jjj = jjj;
  System* kkk=(System*)malloc(sizeof(System));
  kkk = kkk;
  QPoint* lll=(QPoint*)malloc(sizeof(QPoint));
  lll = lll;
  System* mmm=(System*)malloc(sizeof(System));
  mmm = mmm;
  QPoint* nnn=(QPoint*)malloc(sizeof(QPoint));
  nnn = nnn;
  System* ooo=(System*)malloc(sizeof(System));
  ooo = ooo;
  QPoint* ppp=(QPoint*)malloc(sizeof(QPoint));
  ppp = ppp;
  System* qqq=(System*)malloc(sizeof(System));
  qqq = qqq;
  QPoint* rrr=(QPoint*)malloc(sizeof(QPoint));
  rrr = rrr;
  System* sss=(System*)malloc(sizeof(System));
  sss = sss;
  QPoint* ttt=(QPoint*)malloc(sizeof(QPoint));
  ttt = ttt;
  System* uuu=(System*)malloc(sizeof(System));
  uuu = uuu;
  QPoint* vvv=(QPoint*)malloc(sizeof(QPoint));
  vvv = vvv;
  System* www=(System*)malloc(sizeof(System));
  www = www;
  QPoint* xxx=(QPoint*)malloc(sizeof(QPoint));
  xxx = xxx;
  System* yyy=(System*)malloc(sizeof(System));
  yyy = yyy;
  QPoint* zzz=(QPoint*)malloc(sizeof(QPoint));
  zzz = zzz;
  return;
}

// fwd2: system to DOS, without file intermediates
static inline
int getDOS2(System* system,int type,int vec,int N,double dBin) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);
  dirtyHACK(); //XXX magically corrects bin values in DOS calculation

  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  // save to file
  totalDosWrite(nBins,dBin,total);
  if(vec == 1) {
    partialDosWrite(nSites,nBins,dBin,bins);
  }
  int useFiles = 0; // NOTE: allow turn on/off 'intermediate' files
  if(useFiles == 1) {
    qpointWrite("WeightedQ",nq,qs);
    eigenvalueWrite("Omega2",nq,nSites,om2s);
    if(vec == 1) {
      eigenvectorWrite("Polarizations",nq,nSites,pols);
    }
  }
  return 1;
}

// fwd3: system to DOS, without file intermediates, return DOS
static inline
double* getDOS3(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);
  dirtyHACK(); //XXX magically corrects bin values in DOS calculation

  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  // save to file
  int useFiles = 0; // NOTE: allow turn on/off 'intermediate' files
  if(useFiles == 1) {
    qpointWrite("WeightedQ",nq,qs);
    eigenvalueWrite("Omega2",nq,nSites,om2s);
    if(vec == 1) {
      eigenvectorWrite("Polarizations",nq,nSites,pols);
    }
  }
  *nmbins = nBins;
  *pdbins = bins;
  return total;
}

// fwd4: system to DOS, w/o file intermediates, return DOS & intermediates
static inline
double* getDOS4(System* system,int type,int vec,int N,double dBin,
                int* nmbins,double** pdbins,int* nmq,QPoint** qps,
                EigenValue** vs,EigenVector** es) {
  initSetup();

  // get qpoints
  int nq;
  QPoint* qs = generateQpoints(type,system,&nq,N);

  // get eigenvalues & eigenvectors
  EigenVector* pols=NULL;
  EigenValue* om2s = generateEigenValues(vec,system,nq,qs,&pols);
  dirtyHACK(); //XXX magically corrects bin values in DOS calculation
 
  // get DOSs
  int nBins;
  double* bins;
  int nSites = system->c->sites;
  double* total = generateDOS(nSites,nq,qs,om2s,pols,dBin,&nBins,&bins);

  *nmbins = nBins;
  *pdbins = bins;
  *nmq = nq;
  *qps = qs;
  *vs = om2s;
  *es = pols;
  return total;
}

#endif // FWD_H
