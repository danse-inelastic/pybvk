LAPACK_DIR = /tmp/opt/acml-3.6.0/gnu64
#LAPACK_DIR = $(HOME)

CC	= gcc
IFLAGS	= -fpic -I$(LAPACK_DIR)/include
CFLAGS 	= $(IFLAGS) -std=gnu99 -ffast-math -funroll-all-loops -Wall -O3
LDFLAGS	= $(IFLAGS)

LIBS 	= -L$(LAPACK_DIR)/lib -lacml -lacml_mv -lg2c -lm
#LIBS 	= -L$(LAPACK_DIR)/lib/atlas -llapack -L$(HOME)/lib -lg2c -lm
#---------------------------------------------------
SOURCES	= system.c bvk.c h.c pd.c
OBJECTS	= bvk.o system.o
#---------------------------------------------------

all: base h pd

base:
	$(CC) $(CFLAGS) -c $(SOURCES)

h: base
	$(CC) $(LDFLAGS) -o h h.o $(OBJECTS) $(LIBS)

pd: base
	$(CC) $(LDFLAGS) -o pd pd.o $(OBJECTS) $(LIBS)

clean:
	rm -f a.out core *.o
	rm -f ./input-generators/syspy/*.pyc

restore: clean
	rm -f *.pyc _*.so 
	rm -f system WeightedQ dos freqs Polarizations Omega2 DOS*
	rm -f h pd
