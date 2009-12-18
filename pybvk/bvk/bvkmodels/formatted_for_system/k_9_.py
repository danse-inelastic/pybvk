#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=6.49252739954e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 9
reference = 'Dolling, G., Meyer, J.: J. Phys. F7 (1977) 775'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "K", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,0.7688, 0.8805, 0.8805, 
                         0.8805, 0.7688, 0.8805, 
                         0.8805, 0.8805, 0.7688 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.4042, 0.0, 0.0, 
                         0.0, 0.0296, 0.0, 
                         0.0, 0.0, 0.0296 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.0418, -0.0455, 0.0, 
                         -0.0455, -0.0418, 0.0, 
                         0.0, 0.0, 0.0038 ],
[ 0,0,1.5*a,0.5*a,0.5*a,0.0213, 0.0091, 0.0091, 
                         0.0091, -0.0029, 0.003, 
                         0.0091, 0.003, -0.0029 ],
[ 0,0,1.0*a,1.0*a,1.0*a,0.0091, 0.0062, 0.0062, 
                      0.0062, 0.0091, 0.0062, 
                      0.0062, 0.0062, 0.0091 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")