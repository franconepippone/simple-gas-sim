import renderer as gui
import particles as prt
import pygame

#pool.setdomain(((-800,400), (800,-400)))

pool = prt.pool(e = .96, g = 0.01)
pool.setdomain(((400, 200), (800, -200)))

pool2 = prt.pool(e = 1, g = .001)
pool2.setdomain(((-800, 200), (-400, -200)))

pool.random(60, 1, 15, ((450,-150), (750,150)))
pool2.random(60, 20, 15, ((500,-100), (550,100)))


pools = [pool, pool2]

i = 0
while True:
	i+= 1
	pygame.time.Clock().tick(144)

	click = False
	for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            pygame.quit()
	            sys.exit()
	        elif event.type == pygame.MOUSEBUTTONDOWN:
	        	if event.button == 1:
	        		click = True

	if i == 300:
		pool.merge(pool2)
		pool.setdomain(((-800,400), (800,-400)))
		pools.remove(pool2)

	for p in pools:
		p.update()
		print("pool temp: ", p.getmediantemp())
		gui.drawscene(p)

	gui.update()