#!/bin/sh

set -e

eval `use acml`
ACML=/tmp/opt/acml-3.6.0


CC="gcc -std=gnu99 -ffast-math -funroll-all-loops -Wall -O3 -I${ACML}/include"
$CC -c system.c
$CC -c bvk.c

#$CC -c fwd.c
#gcc -o fwd fwd.o bvk.o system.o -L${ACML}/lib -lacml -lg2c -lm

$CC -c h.c
gcc -o h h.o bvk.o system.o -L${ACML}/lib -lacml -lg2c -lm

$CC -c pd.c
gcc -o pd pd.o bvk.o system.o -L${ACML}/lib -lacml -lg2c -lm

$CC -c randomQs.c
gcc -o randomQs randomQs.o bvk.o system.o -L${ACML}/lib -lacml -lg2c -lm

$CC -c regularQs.c
gcc -o regularQs regularQs.o bvk.o system.o -L${ACML}/lib -lacml -lg2c -lm
