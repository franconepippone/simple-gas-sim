import renderer as gui
import particles as prt
import pygame


# Creates first pool object
pool = prt.pool(e = 1, g = .05)
pool.setdomain(((-200, 500), (200, -500)))
piston = prt.piston('x',0,500,400,100)
pool.add(piston)
pool.random(100, 1, 15, rect = ((-200, 300), (200, -500)))

mouse_pos = {'x':0, 'y':0}
draggable = prt.grabparticle(mouse_pos, 30)
pool.add(draggable)


def merge():
	pool.setdomain(((-800,400), (800,-400)))
	piston.changelen(1600)
	pool.e = .99

def store_mouse(pos):
	mouse_pos['x'] = pos[0]
	mouse_pos['y'] = pos[1]

click = False
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
				merge()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	store_mouse(gui.truemouse(pygame.mouse.get_pos()))
	
	pool.update()
	gui.drawpool(pool)

	gui.update() # Updates screen