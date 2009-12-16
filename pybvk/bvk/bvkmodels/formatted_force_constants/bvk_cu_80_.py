#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.05529724344e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 80
reference = 'Nilsson, G., Rolandson, S.: Phys. Rev. B7 (1973) 2393'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Cu", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,13.57, 15.542, 0.0, 
                         15.542, 13.57, 0.0, 
                         0.0, 0.0, -1.078 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.199, 0.0, 0.0, 
                         0.0, -0.209, 0.0, 
                         0.0, 0.0, -0.209 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.442, 0.217, 0.217, 
                         0.217, 0.315, 0.113, 
                         0.217, 0.113, 0.315 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.112, 0.226, 0.0, 
                         0.226, 0.112, 0.0, 
                         0.0, 0.0, -0.1 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.223, 0.084, 0.0, 
                         0.084, -0.02, 0.0, 
                         0.0, 0.0, -0.186 ],
[ 0,0,2.0*a,2.0*a,2.0*a,-0.141, -0.126, -0.126, 
                      -0.126, -0.141, -0.126, 
                      -0.126, -0.126, -0.141 ],
[ 0,0,3.0*a,2.0*a,1.0*a,0.022, 0.034, -0.04, 
                      0.034, 0.1, -0.006, 
                      -0.04, -0.006, -0.031 ],
[ 0,0,4.0*a,0.0*a,0.0*a,0.016, 0.0, 0.0, 
                      0.0, 0.123, 0.0, 
                      0.0, 0.0, 0.123 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
