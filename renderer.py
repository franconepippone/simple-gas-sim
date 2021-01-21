import pygame, os
import time
import particles as prt

pygame.init()

# inizializzazione pygame e finestra

WIDTH, HEIGHT = 1920, 1080
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE = 255,255,255
os.environ['SDL_VIDEO_CENTERED'] = '1'
schermo = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption('particles')

schermo.fill(WHITE)


def update(background = WHITE):
	pygame.display.update()
	schermo.fill(background)

def drawwidgets(*items):
	for item in items:
		if type(item) == prt.slider:
			pygame.draw.line(schermo, (100,100,100), (int(item.x0) + OFFW, -int(item.y) + OFFH), (int(item.x1) + OFFW, -int(item.y) + OFFH), 8)
			pygame.draw.circle(schermo, item.color, (int(item.x) + OFFW, -int(item.y) + OFFH), int(item.size))

def drawpool(pool):
	for p in pool.particles:
		pygame.draw.circle(schermo, p.color, (int(p.x) + OFFW, -int(p.y) + OFFH), int(p.r))

	for b in pool.obstacles:
		if type(b) == prt.barrier or type(b) == prt.piston or type(b) == prt.heatplate:
			if b.axys == 1:
				pygame.draw.line(schermo, b.color, (int(b.x0) + OFFW, -int(b.y) + OFFH), (int(b.x1) + OFFW, -int(b.y) + OFFH), 15)
			elif b.axys == 0:
				pygame.draw.line(schermo, b.color, (int(b.x) + OFFW, -int(b.y0) + OFFH), (int(b.x) + OFFW, -int(b.y1) + OFFH), 4)
		elif type(b) == prt.box:
			pygame.draw.rect(schermo, b.color, offsetrect(b, OFFW, OFFH), 2)

	pygame.draw.rect(schermo, pool.cont.color, offsetrect(pool.cont, OFFW, OFFH), 2)

def offsetrect(rect, dx, dy):
	return (rect.x0 + dx, -rect.y0 + dy), (rect.x1 - rect.x0, -rect.y1 + rect.y0)

def truemouse(pos):
	return pos[0] - OFFW, pos[1] - OFFH