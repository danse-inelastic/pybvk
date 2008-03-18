CFLAGS=-O3 -Wall
LIBS=

OBJS = h.o 

h: $(OBJS)
	g++ -o h $(OBJS) $(LIBS)

.C.o: $<
	g++ $(CFLAGS) -c $<

clean:
	rm -f h $(OBJS)

neat:
	rm -f *.o

h.o:
