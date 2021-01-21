## WIP (just messing around)

## New features:
##### _class_ particles.grabparticle(_mouse, r_)
  - Returns a particle object that can be added to a pool. 'mouse' is a reference to a dictionary containing mouse coordinates, 'r' is radius
##### _class_ particles.heatplate(_axys, widget, x, y, l, tag=None_)
  - Same as barrier, takes a widget object (slider) for updating
##### _class_ particles.piston(_axys, x, y, l, m, tag = None_)
  - Same as barrier, supports rigid body interactions with particles (horizontal axys only supported)
##### pool.slider(_x, y, range, lenght, size_)
  - Creates a slider object that can be drawn using the _renderer.drawwidgets(*widgets)_ function. See code for implementation.
