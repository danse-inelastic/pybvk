SYS_DIR = ../../systems
SYM_DIR = ./syms
#---------------------------------------------------
SYSTEMS	= Al Al8 Al_conv Ce Fe FeCube Ho In Mg Ni NiAl Sc Tb V3Si \
          V3Si.S0 V3Si.S1 Zr
GENSYMS = cubic hcp fct identity
#---------------------------------------------------

all: system

symmetry:
	for s in $(GENSYMS); do (./symWrite.py $${s}); done

system: symmetry
	mkdir -p $(SYS_DIR)
	for s in $(SYSTEMS); do (./$${s}; mv system $(SYS_DIR)/$${s}); done

clean:
	rm -f a.out core *.o
	rm -f *.pyc system

restore: clean
	rm -f *.pyc _*.so 
	rm -rf $(SYS_DIR) $(SYM_DIR)
