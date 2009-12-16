#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=1.15260710727e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 293
reference = 'Beg, M.M., Nielsen, M.: Phys. Rev. B14 (1976) 4266'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Li", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,2.114, 2.207, 2.207, 
                         2.207, 2.114, 2.207, 
                         2.207, 2.207, 2.114 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.862, 0.0, 0.0, 
                         0.0, 0.016, 0.0, 
                         0.0, 0.0, 0.016 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.268, -0.197, 0.0, 
                         -0.197, -0.268, 0.0, 
                         0.0, 0.0, 0.055 ],
[ 0,0,1.5*a,0.5*a,0.5*a,0.146, 0.052, 0.052, 
                         0.052, -0.057, 0.033, 
                         0.052, 0.033, -0.057 ],
[ 0,0,1.0*a,1.0*a,1.0*a,0.062, 0.077, 0.077, 
                      0.077, 0.062, 0.077, 
                      0.077, 0.077, 0.062 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
