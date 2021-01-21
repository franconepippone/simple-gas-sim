import renderer as gui
import particles as prt
import pygame


# Creates first pool object
pool = prt.pool(e = .99, g = .01)
pool.setdomain(((400, 200), (800, -200)))

# Creates second pool object
pool2 = prt.pool(e = 1, g = .001)
pool2.setdomain(((-800, 200), (-400, -200)))

mouse_pos = {'x':0, 'y':0}
draggable = prt.grabparticle(mouse_pos, 30)
pool.add(draggable)

# Initializes particles randomly
pool.random(60, 1, 15)
pool2.random(60, 20, 15)


def store_mouse(pos):
	mouse_pos['x'] = pos[0]
	mouse_pos['y'] = pos[1]

pools = [pool, pool2]

i = 0
while True:
	i+= 1
	pygame.time.Clock().tick(144)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_SPACE:
				pool.merge(pool2)
				pool.setdomain(((-800,400), (800,-400)))
				pools.remove(pool2)
				pool.e = .9

	store_mouse(gui.truemouse(pygame.mouse.get_pos()))
					
	# Updates and renders all pools
	for p in pools:
		p.update()
		print("pool temp: ", p.getmediantemp())   # Gets median 'temperature' (Velocity) of particles in pool
		gui.drawpool(p)

	gui.update() # Updates screen