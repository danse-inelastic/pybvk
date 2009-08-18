#LAPACK_DIR = /tmp/opt/acml-3.6.0/gnu64
##LAPACK_DIR = /tmp/opt/acml4gf-4.1.0/gfortran64
LAPACK_DIR = $(HOME)

CC	= g++
IFLAGS	= -fpic -I$(LAPACK_DIR)/include
CFLAGS 	= $(IFLAGS) -ffast-math -funroll-all-loops -Wall -O3
LDFLAGS	= $(IFLAGS)

#LIBS 	= -L$(LAPACK_DIR)/lib -lacml -lacml_mv -lm
##LIBS 	= -L$(LAPACK_DIR)/lib -lacml -lacml_mv -lm -lgfortran
LIBS 	= -L$(LAPACK_DIR)/lib/atlas -llapack -L$(HOME)/lib -lm
#---------------------------------------------------
SOURCES	= system.c bvk.c fwd.c h.c pd.c randomQs.c regularQs.c \
          printQs.c printEVs.c printDOS.c printSys.c
OBJECTS	= bvk.o system.o
#---------------------------------------------------

all: fwd

steps: h pd randomQs regularQs 

systems:
	cd input-generators/syspy ; make ; make clean ; cd ../..

base:
	$(CC) $(CFLAGS) -c $(SOURCES)

fwd: base
	$(CC) $(LDFLAGS) -o fwd fwd.o $(OBJECTS) $(LIBS)

h: base
	$(CC) $(LDFLAGS) -o h h.o $(OBJECTS) $(LIBS)

pd: base
	$(CC) $(LDFLAGS) -o pd pd.o $(OBJECTS) $(LIBS)

randomQs: base
	$(CC) $(LDFLAGS) -o randomQs randomQs.o $(OBJECTS) $(LIBS)

regularQs: base
	$(CC) $(LDFLAGS) -o regularQs regularQs.o $(OBJECTS) $(LIBS)

inspect: base
	$(CC) $(LDFLAGS) -o printQs printQs.o $(OBJECTS) $(LIBS)
	$(CC) $(LDFLAGS) -o printEVs printEVs.o $(OBJECTS) $(LIBS)
	$(CC) $(LDFLAGS) -o printDOS printDOS.o $(OBJECTS) $(LIBS)
	$(CC) $(LDFLAGS) -o printSys printSys.o $(OBJECTS) $(LIBS)

clean:
	rm -f a.out core *.o
	rm -f ./input-generators/syspy/*.pyc
	rm -f ./input-generators/qs/*/h
	rm -f ./input-generators/qs/cubicMPGrid/out

restore: clean
	rm -f *.pyc _*.so 
	rm -f fwd h pd randomQs regularQs printQs printEVs printDOS printSys
	rm -f system WeightedQ dos freqs Polarizations Omega2 DOS*
	cd input-generators/syspy ; make restore ; cd ../..
