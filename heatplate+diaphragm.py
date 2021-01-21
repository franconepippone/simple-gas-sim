import renderer as gui
import particles as prt
import pygame


# Creates first pool object
pool = prt.pool(e = .9, g = .05)
pool.setdomain(((-300, 500), (300, -500)))
pool.add(prt.piston('x',0,300,600,100))
pool.random(60, 1, 15, rect = ((-200, 300), (200, -500)))

# Creating slider
slider = prt.slider(500,0,(0,100),200, 20)
# Adding heatplate to pool
pool.add(prt.heatplate(slider,'x',  0, -500, 600))



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
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	pool.update()
	gui.drawpool(pool)

	slider.update(gui.truemouse(pygame.mouse.get_pos()), click)
	gui.drawwidgets(slider)

	gui.update() # Updates screen
