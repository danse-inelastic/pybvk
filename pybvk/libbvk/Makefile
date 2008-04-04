#LAPACK_DIR = /tmp/opt/acml-3.6.0/gnu64
##LAPACK_DIR = /opt/acml4.0.1/gfortran64_int64
LAPACK_DIR = $(HOME)

CC	= gcc
IFLAGS	= -fpic -I$(LAPACK_DIR)/include
CFLAGS 	= $(IFLAGS) -std=gnu99 -ffast-math -funroll-all-loops -Wall -O3
LDFLAGS	= $(IFLAGS)

#LIBS 	= -L$(LAPACK_DIR)/lib -lacml -lacml_mv -lg2c -lm
##LIBS 	= -L$(LAPACK_DIR)/lib -lacml -lacml_mv -lg2c -lm -lgfortran
LIBS 	= -L$(LAPACK_DIR)/lib/atlas -llapack -L$(HOME)/lib -lg2c -lm
#---------------------------------------------------
SOURCES	= system.c bvk.c fwd.c h.c pd.c randomQs.c regularQs.c \
          printQs.c printEVs.c
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

clean:
	rm -f a.out core *.o
	rm -f ./input-generators/syspy/*.pyc
	rm -f ./input-generators/qs/*/h
	rm -f ./input-generators/qs/cubicMPGrid/out

restore: clean
	rm -f *.pyc _*.so 
	rm -f fwd h pd randomQs regularQs printQs printEVs
	rm -f system WeightedQ dos freqs Polarizations Omega2 DOS*
	cd input-generators/syspy ; make restore ; cd ../..
