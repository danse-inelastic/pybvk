#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.76718698107e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 673
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
[ 0,0,1.0*a,1.0*a,0.0*a,17.599, 21.35, 0.0, 
                         21.35, 17.599, 0.0, 
                         0.0, 0.0, -2.412 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.39, 0.0, 0.0, 
                         0.0, 0.044, 0.0, 
                         0.0, 0.0, 0.044 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.661, 0.784, 0.784, 
                         0.784, 0.388, 0.039, 
                         0.784, 0.039, 0.388 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.72, -1.283, 0.0, 
                         -1.283, -0.72, 0.0, 
                         0.0, 0.0, -0.177 ],
[ 0,0,3.0*a,1.0*a,0.0*a,0.217, 0.167, 0.0, 
                         0.167, -0.228, 0.0, 
                         0.0, 0.0, -0.284 ],
[ 0,0,2.0*a,2.0*a,2.0*a,-0.063, 0.116, 0.116, 
                      0.116, -0.063, 0.116, 
                      0.116, 0.116, -0.063 ],
[ 0,0,3.0*a,2.0*a,1.0*a,-0.139, -0.09, -0.045, 
                      -0.09, 0.155, -0.03, 
                      -0.045, -0.03, 0.012 ],
[ 0,0,4.0*a,0.0*a,0.0*a,0.071, 0.0, 0.0, 
                      0.0, 0.028, 0.0, 
                      0.0, 0.0, 0.028 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")