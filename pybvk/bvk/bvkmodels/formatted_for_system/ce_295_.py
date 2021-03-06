#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=2.32673530389e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 80
reference = 'Stassis, C., Gould, T., McMasters, O.D., Gschneider, K.A., Nicklow, R.M.: Phys. Rev B19 (1979) 5746'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Ce", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,4.3726, 4.5798, 0.0, 
                         4.5798, 4.3726, 0.0, 
                         0.0, 0.0, -0.2264 ],
[ 0,0,2.0*a,0.0*a,0.0*a,-2.3562, 0.0, 0.0, 
                         0.0, 0.0773, 0.0, 
                         0.0, 0.0, 0.0773 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.2058, -0.0496, -0.0496, 
                         -0.0496, 0.3169, -0.0547, 
                         -0.0496, -0.0547, 0.3169 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.1231, 0.1505, 0.0, 
                         0.1505, 0.1231, 0.0, 
                         0.0, 0.0, 0.0114 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.0525, 0.0193, 0.0, 
                         0.0193, -0.0992, 0.0, 
                         0.0, 0.0, -0.1044 ],
[ 0,0,2.0*a,2.0*a,2.0*a,-0.3316, -0.2194, -0.2194, 
                      -0.2194, -0.3316, -0.2194, 
                      -0.2194, -0.2194, -0.3316 ],
[ 0,0,3.0*a,2.0*a,1.0*a,0.1057, -0.0068, 0.0763, 
                      -0.0068, -0.1138, 0.005, 
                      0.0763, 0.005, 0.0263 ],
[ 0,0,4.0*a,0.0*a,0.0*a,-0.0009, 0.0, 0.0, 
                      0.0, 0.2219, 0.0, 
                      0.0, 0.0, 0.2219 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
