import math
from random import randint, uniform
from numpy import sign


class particle:
	def __init__(self, pos, vel, r):
		self.x = pos[0]
		self.y = pos[1]
		self.xv = vel[0]
		self.yv = vel[1]
		self.r = r
		self.color = (255,0,0)
		self.container = None
		self.m = 1

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

class grabparticle(particle):
	def __init__(self, mouse, r):
		super(grabparticle, self).__init__((0,0), (0,0), r)
		self.mouse = mouse
		self.color = (100,100,255)
		self.speed = 1

	def update(self, G):
		self.xv = self.mouse['x'] - self.x
		self.yv = -self.mouse['y'] - self.y
		self.x += self.xv
		self.y += self.yv

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
	updatable = False
	e = 1
	tag = None
	def collide(self, p, E):
		pass

class slider:
	def __init__(self, x, y, range, lenght, size):
		self.x0 = x - lenght / 2
		self.x1 = x + lenght / 2
		self.y = y
		self.x = self.x0
		self.value = 0
		self.start = range[0]
		self.end = range[1]
		self.range = range[1] - range[0]
		self.size = size
		self.color = (150,150,150)

	def update(self, mouse_pos, clicking):
		mx, my = mouse_pos
		# if colliding with mouse
		if self.x - self.size <= mx <= self.x + self.size and self.y - self.size <= my <= self.y + self.size:
			self.color = (200,200,200)
			if clicking:
				self.x = mx
				if self.x > self.x1:
					self.x = self.x1
				elif self.x < self.start + self.x0:
					self.x = self.start + self.x0
			self.value = (self.x - self.x0) / self.range
		else:
			self.color = (100,100,100)

class barrier(obstacle):
	def __init__(self, axys, x, y, l, tag = None):
		self.tag = tag
		if axys == 1 or axys == 'x':
			self.axys = 1
			self.y = y
			self.x_ = x
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axys == 0 or axys == 'y':
			self.axys = 0
			self.x = x
			self.y_ = y
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("invalid axys")

	def changelen(self, l):
		if self.axys == 1:
			self.x0 = self.x_ - l/2
			self.x1 = self.x_ + l/2
		else:
			self.y0 = self.y_ - l/2
			self.y1 = self.y_ + l/2

	def collide(self, p, E):
		if self.axys == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect * sign(p.yv)
				p.yv = - p.yv * E * self.e
		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * sign(p.xv)
				p.xv = - p.xv * E * self.e

class heatplate(barrier):
	updatable = True
	def __init__(self, widget, axys, x, y, l, tag = None):
		super(heatplate, self).__init__(axys, x, y, l, tag)
		self.widget = widget
		self.e = 1
		self.color = (0,0,0)

	def update(self, _):
		print("calling")
		self.e = self.widget.value * 2
		self.color = getcolor(self.e * 3.75)

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
	updatable = True
	def __init__(self, axys, x, y, l, m, tag = None):
		self.tag = tag
		self.v = 0
		self.m = m
		if axys == 1 or axys == 'x':
			self.axys = 1
			self.y = y
			self.x_ = x
			self.x0 = x - l/2
			self.x1 = x + l/2
		elif axys == 0 or axys == 'y':
			self.axys = 0
			self.x = x
			self.y_ = y
			self.y0 = y - l/2
			self.y1 = y + l/2
		else:
			print("invalid axys")

	def update(self, g):
		if self.axys == 1:
			self.v -= g
			self.y += self.v
		else:
			self.y += self.v

	def changelen(self, l):
		if self.axys == 1:
			self.x0 = self.x_ - l/2
			self.x1 = self.x_ + l/2
		else:
			self.y0 = self.y_ - l/2
			self.y1 = self.y_ + l/2

	def collide(self, p, E):
		if self.axys == 1:
			intersect = abs(p.y - self.y) - p.r
			if self.x0 < p.x < self.x1 and intersect < 0:
				p.y += intersect
				#self.y -= intersect / 2
				dv = (self.v - p.yv) *2 
				self.v -= dv / (1 + self.m)
				p.yv += (dv * self.m) / (1 + self.m)

		else:
			intersect = abs(p.x - self.x) - p.r
			if self.y0 < p.y < self.y1 and intersect < 0:
				p.x += intersect * sign(p.xv)
				p.xv = - p.xv * E * self.e

class pool:

	def __init__(self, e = 1, g = 0, *particles):
		self.particles = []
		self.obstacles = []
		self.updatables = []
		self.cont = _container(((-10000,10000), (10000,-10000)))
		self.e, self.g = e, g
		for p in particles:
			self.add(p)

	def add(self, body):
		if issubclass(type(body), obstacle) or type(body) == heatplate:
			self.obstacles.append(body)
			if body.updatable == True:
				self.updatables.append(body)
		elif issubclass(type(body), particle):
			self.particles.append(body)
			self.updatables.append(body)

	def merge(self, pool2):
		self.particles += pool2.particles
		self.obstacles += pool2.obstacles
		self.updatables += pool2.updatables

	def update(self):
		e = self.e *.5 + .5
		for body in self.updatables:
			body.update(self.g)
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
		self.updatables = [item for item in self.updatables if item.tag != tag]

	def random(self, n, v, r, rect = None):
		if rect is None:
			rect = self.cont.rect
			print(rect)
		for _ in range(n):
			p = particle((randint(rect[0][0], rect[1][0]), randint(rect[1][1], rect[0][1])), (uniform(-v, v), uniform(-v, v)), r)
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
		newpool.updatables += p.updatables
	return newpool