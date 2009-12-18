#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.76718698107e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 296
reference = 'Miiller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Pd", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,19.337, 22.423, 0.0, 
                         22.423, 19.337, 0.0, 
                         0.0, 0.0, -2.832 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.424, 0.0, 0.0, 
                         0.0, 0.21, 0.0, 
                         0.0, 0.0, 0.21 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.744, 0.708, 0.708, 
                         0.708, 0.249, 0.163, 
                         0.708, 0.163, 0.249 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-1.142, -1.37, 0.0, 
                         -1.37, -1.142, 0.0, 
                         0.0, 0.0, -0.223 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.006, 0.076, 0.0, 
                         0.076, -0.207, 0.0, 
                         0.0, 0.0, -0.232 ],
[ 0,0,2.0*a,2.0*a,2.0*a,0.154, 0.33, 0.33, 
                      0.33, 0.154, 0.33, 
                      0.33, 0.33, 0.154 ],
[ 0,0,3.0*a,2.0*a,1.0*a,0.07, -0.065, -0.032, 
                      -0.065, 0.067, -0.022, 
                      -0.032, -0.022, -0.02 ],
[ 0,0,4.0*a,0.0*a,0.0*a,0.072, 0.0, 0.0, 
                      0.0, 0.006, 0.0, 
                      0.0, 0.0, 0.006 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")