#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=4.48049468615e-26   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 80
reference = 'Cowley, E.R.: Can. J. Phys. 52 (1974) 1714'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Al", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,10.4578, 10.3657, 0.0, 
                         10.3657, 10.4578, 0.0, 
                         0.0, 0.0, -2.6322 ],
[ 0,0,2.0*a,0.0*a,0.0*a,2.4314, 0.0, 0.0, 
                         0.0, -0.1351, 0.0, 
                         0.0, 0.0, -0.1351 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.0986, -0.1819, -0.1819, 
                         -0.1819, -0.2366, -0.2862, 
                         -0.1819, -0.2862, -0.2366 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.1363, 0.3753, 0.0, 
                         0.3753, 0.1363, 0.0, 
                         0.0, 0.0, 0.1854 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.3003, -0.3239, 0.0, 
                         -0.3239, 0.1842, 0.0, 
                         0.0, 0.0, 0.2603 ],
[ 0,0,2.0*a,2.0*a,2.0*a,-0.1412, 0.199, 0.199, 
                      0.199, -0.1412, 0.199, 
                      0.199, 0.199, -0.1412 ],
[ 0,0,3.0*a,2.0*a,1.0*a,0.1828, 0.0397, -0.0747, 
                      0.0397, -0.2207, -0.0214, 
                      -0.0747, -0.0214, -0.0173 ],
[ 0,0,4.0*a,0.0*a,0.0*a,-0.0681, 0.0, 0.0, 
                      0.0, -0.0202, 0.0, 
                      0.0, 0.0, -0.0202 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
