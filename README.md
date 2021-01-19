# Simple-gas-sim

Simple particle gas simulation made with python and pygame.  

## Features:
##### _class_ particles.particle(_pos, vel, r_)
  - Returns a particle object that can be added to a pool. 'pos' and 'vel' are both tuples
##### _class_ particles.barrier(_paxys, x, y, l, tag=None_)
  - Returns a barrier object that can be added to a pool. 'axys' defines barrier orientation (1: Horizontal; 0: Vertical), 'l' defines lenght
  - A tag might be added to target the barrier once added to a pool.

##### _class_ particles.pool(_e=1, g=0, *particles_)
  - Returns a pool object that can run a particle simulation. 'e' defines collision elasticity, 'g' defines gravity.
##### pool.setdomain(_rect_)
  - Defines simulation bounding box. Rect is expressed as a tuple: ((_top-left-corner_), (_bottom-right-corner_))
##### pool.random(_n, v, r, rect=None_)
  - Creates 'n' random particles with 'r' radius. 'v' defines maximum speed, 'rect' defines particle spawn area (Defaults to pool domain)
##### pool.add(_body_)
  - Adds particle/obstacle to pool
##### pool.merge(_pool2_)
  - Merges contents of pool2 with pool
##### pool.update()
  - Advances simulation of one timestep
