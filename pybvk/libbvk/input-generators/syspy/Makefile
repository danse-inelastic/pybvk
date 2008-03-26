SYSDIR = ../../systems
#---------------------------------------------------
SYSTEMS	= Al Al8 Al_conv Ce Fe FeCube Ho In Mg Ni NiAl Sc Tb V3Si \
          V3Si.S0 V3Si.S1 Zr
#---------------------------------------------------

all: system

system: 
	mkdir -p $(SYSDIR)
	for sys in $(SYSTEMS) ; do (./$${sys} ; mv system $(SYSDIR)/$${sys}); done

clean:
	rm -f a.out core *.o
	rm -f *.pyc system

restore: clean
	rm -f *.pyc _*.so 
	rm -rf $(SYSDIR)
