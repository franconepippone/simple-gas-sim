import math
from random import randint, uniform
import numpy


class particle:
	def __init__(self, pos, vel, r):
		self.x = pos[0]
		self.y = pos[1]
		self.xv = vel[0]
		self.yv = vel[1]
		self.r = r
		self.color = (255,0,0)
		self.container = None

	def update(self, G):
		self.yv -= G
		self.x += self.xv
		self.y += self.yv
		self.speed = math.sqrt(self.xv**2 + self.yv**2)
		self.color = getcolor(self.speed)

	def collide(self, body, E):
		dx, dy = self.x - body.x, self.y - body.y
		d = math.sqrt(dx**2 + dy**2)

		if d < self.r + body.r:
			dvx, dvy = self.xv - body.xv, self.yv - body.yv
			sin, cos = dx/d, dy/d 
			dr = (self.r + body.r - d) / 2
			dx2, dy2 = sin * dr, cos * dr

			self.x += dx2
			self.y += dy2
			body.x -= dx2
			body.y -= dy2

			h = (dx * dvx + dy * dvy) / d
			new_dvx, new_dvy = -h * sin * E, -h * cos * E

			self.xv += new_dvx
			self.yv += new_dvy
			body.xv -= new_dvx
			body.yv -= new_dvy

def clamp(n, min, max):
	if min < n < max:
		return n
	elif n >= max:
		return max
	else:
		return min

def mixrgb(fac, rgb1, rgb2):
	return tuple([c2*fac + c1*(1-fac) for c1, c2 in zip(rgb1, rgb2)])

def getcolor(speed):
	return mixrgb(clamp(speed/15, 0, 1), (0,0,255), (255,0,0))

class obstacle:
	color = (0,0,0)
	e = 1
	tag = None
	def collide(self, p, E):
		pass

class barrier(obstacle):
	def __init__(self, axys, x, y, l, tag = None):
		self.tag = tag
		if axys == 1 or axys == 'x':
			self.axys = 1
			self.y = y
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axys == 0 or axys == 'y':
			self.axys = 0
			self.x = x
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("invalid axys")

	def collide(self, p, E):
		if self.axys == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect * numpy.sign(p.yv)
				p.yv = - p.yv * E * self.e
		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * numpy.sign(p.xv)
				p.xv = - p.xv * E * self.e

class _container(obstacle):
	def __init__(self, rect):
		self.rect = rect
		self.x0 = rect[0][0]
		self.y0 = rect[0][1]
		self.x1 = rect[1][0]
		self.y1 = rect[1][1]

	def collide(self, p, E):
		if p.y + p.r > self.y0:
			p.y -= p.r + p.y - self.y0
			p.yv = -p.yv * E
		elif p.y - p.r < self.y1:
			p.y += p.r - p.y + self.y1
			p.yv = -p.yv * E
		if p.x + p.r > self.x1:
			p.x -= p.r + p.x - self.x1
			p.xv = -p.xv * E
		elif p.x - p.r < self.x0:
			p.x += p.r - p.x + self.x0
			p.xv = -p.xv * E

class box(obstacle):
	def __init__(self, rect, tag = None):
		self.rect = rect
		self.x0 = rect[0][0]
		self.y0 = rect[0][1]
		self.x1 = rect[1][0]
		self.y1 = rect[1][1]
		self.tag = tag

	def collide(self, p, E):
		if self.x0 <= p.x <= self.x1 and self.y1 <= p.y <= self.y0:
			if self.y1 <= p.y <= self.y0:
				if p.yv > 0:
					pass
				p.yv = -p.yv * E
			if self.x0 <= p.x <= self.x1:
				pass

class piston(obstacle):
	def __init__(self, axys, x, y, l, tag = None):
		self.tag = tag
		self.v = 0
		if axys == 1 or axys == 'x':
			self.axys = 1
			self.y = y
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axys == 0 or axys == 'y':
			self.axys = 0
			self.x = x
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("invalid axys")

	def collide(self, p, E):
		if self.axys == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect * numpy.sign(p.yv)
				p.yv = - p.yv * E * self.e
				self.v
		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * numpy.sign(p.xv)
				p.xv = - p.xv * E * self.e

class pool:

	def __init__(self, e = 1, g = 0, *particles):
		self.particles = []
		self.obstacles = []
		self.cont = _container(((-10000,10000), (10000,-10000)))
		self.e, self.g = e, g
		for p in particles:
			self.add(p)

	def add(self, body):
		if issubclass(type(body), obstacle):
			self.obstacles.append(body)
		elif type(body) == particle:
			self.particles.append(body)

	def merge(self, pool2):
		self.particles += pool2.particles
		self.obstacles += pool2.obstacles

	def update(self):
		e = self.e *.5 + .5
		for p in self.particles:
			p.update(self.g)
		for i, p in enumerate(self.particles):
			for p2 in self.particles[i+1:]:
				p.collide(p2, e)

			for b in self.obstacles:
				b.collide(p, e)
			self.cont.collide(p, e)

	def setdomain(self, rect):
		self.cont = _container(rect)

	def getmediantemp(self):
		t = 0
		for p in self.particles:
			t += p.speed
		try:
			t /= len(self.particles)
			return t
		except ZeroDivisionError:
			print("Pool is empty, cannot get temperature.")

	def removeob(self, tag):
		self.obstacles = [item for item in self.obstacles if item.tag != tag]

	def random(self, n, s, r, rect):
		for _ in range(n):
			p = particle((randint(rect[0][0], rect[1][0]), randint(rect[0][1], rect[1][1])), (uniform(-s, s), uniform(-s, s)), r)
			self.add(p)


def mergepools(*pools, e = False, g = False):
	if not e:
		e = pools[0].e
	if not g:
		g = pools[0].g
	newpool = pool(e = e, g = g)
	for p in pools:
		newpool.particles += p.particles
		newpool.obstacles += p.obstacles
	return newpool