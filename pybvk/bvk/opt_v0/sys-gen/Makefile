SYM_DIR = ./syms
PATH_0 = ../../../libbvk/input-generators/syspy
TARGET_0 = symWrite.py symmetries.py System.py
#---------------------------------------------------
GENSYMS = cubic hcp fct identity
#---------------------------------------------------

all: fetch symmetry

fetch:
	for s in $(TARGET_0); do (cp -f $(PATH_0)/$${s} .); done

symmetry:
	for s in $(GENSYMS); do (./symWrite.py $${s}); done

clean:
	rm -f a.out core *.o *.pyc system

restore: clean
	rm -f _*.so 
	rm -rf $(SYM_DIR)

tidy: restore
	rm -f System.py symmetries.py symWrite.py

