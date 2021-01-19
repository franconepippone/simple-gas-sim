import pygame 
import time

pygame.init()

# inizializzazione pygame e finestra

WIDTH, HEIGHT = 1920, 1080
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255

schermo = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

pygame.display.set_caption('particles')

schermo.fill(WHITE)


def update(background = WHITE):
	pygame.display.update()
	schermo.fill(background)

def drawscene(pool):
	for p in pool.particles:
		pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

	for b in pool.obstacles:
		if type(b) == prt.barrier:
			if b.axys == 1:
				pygame.draw.line(schermo, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 4)
			elif b.axys == 0:
				pygame.draw.line(schermo, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)
		elif type(b) == prt.box:
			pygame.draw.rect(schermo, b.color, offsetrect(b, OFFW, OFFH), 2)

	pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
	return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)