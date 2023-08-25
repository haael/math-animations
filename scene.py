#!/usr/bin/python3


import cairo
from math import *
from asyncio import sleep, gather, create_task, run, CancelledError

from shapes import *
from animations import *



class Animation:
	def __init__(self, bg_anim=None):
		self.running = True
		self.finished = False
		self.bg_anim = bg_anim
		self.take_animations = []
		self.take_no = 0
	
	def take(self, take):
		self.take_animations.append(take)
		return take
	
	async def animate(self, scene):
		await gather(self.animate_background(scene), self.animate_foreground(scene))
	
	async def animate_foreground(self, scene):
		self.take_no = 0
		while not self.finished:
			self.__take = create_task(self.animate_take(scene))
			await self.__take
	
	async def animate_background(self, scene):
		while not self.finished:
			if self.running:
				self.__bg = create_task(self.bg_anim(scene))
			else:
				self.__bg = create_task(sleep(1))
			
			try:
				await self.__bg
			except CancelledError:
				pass
	
	async def animate_take(self, scene):
		try:
			if self.running:
				if 0 <= self.take_no < len(self.take_animations):
					await self.take_animations[self.take_no](scene)
				else:
					self.finished = True
			else:
				await sleep(1)
		except CancelledError:
			pass
		else:
			if self.running:
				self.take_no += 1
	
	def pause(self):
		self.running = False
		self.__bg.cancel()
		self.__take.cancel()
	
	def resume(self):
		self.running = True
		self.__bg.cancel()
		self.__take.cancel()
	
	def stop(self):
		self.finished = True
		self.__bg.cancel()
		self.__take.cancel()


async def animate_button(scene, name='animate_button'):
	group = Circle(100, scene.scene_width / 2, 0, '#800', '#f0f', alpha=0)
	scene[name] = group
	await sleep(0.5)
	
	await gather(
		translate(group, 0, scene.scene_height / 2, 1.5),
		fadein(group, 1.5)
	)
	
	group['one'] = Circle(10, 0, 20, '#0f0', '#0ff', alpha=0)
	group['two'] = Circle(10, 0, -20, '#0f0', '#0ff', alpha=0)
	group['three'] = Circle(10, 20, 0, '#0f0', '#0ff', alpha=0)
	group['four'] = Circle(10, -20, 0, '#f00', '#f00', alpha=0)
	
	await gather(
		fadein(group['one'], 0.5),
		fadein(group['two'], 1),
		fadein(group['three'], 1.5),
		fadein(group['four'], 2)
	)
	await rotate(group, pi / 2, 1)
	await sleep(1)
	await fadeout(group, 1.5)
	await sleep(1)
	del scene[name]


async def animate_complex_plane(scene, name='animate_complex_plane'):
	group = Actor(scene.scene_width / 2, scene.scene_height / 2, None, None)
	scene[name] = group
	
	group['central_point'] = Circle(2.5, 0, 0, '#000', '#000')
	
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#000', 0)
	group['line_r'] = line_r
	await sleep(1.2)
	
	for n in range(20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#000', pi/2)
		line_r['n' + str(n)] = Text(str(n), 20, 50 * n, -25, '#000')
		await sleep(0.05)
	await sleep(1.2)
	
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#00f', 0)
	neg_numbers = Actor(0, 0, None, None, alpha=0)
	for n in range(20):
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#00f', pi/2)
		if n > 0:
			neg_numbers['n' + str(n)] = NonrotatedText(str(-n), 20, 50 * n, -25, '#00f')
	line_l['neg_numbers'] = neg_numbers
	group['line_l'] = line_l
	
	await gather(fadein(neg_numbers, 1.5), rotate(line_l, -pi, 1.5))
	await sleep(2)
	
	complex_line = Circle(0, 0, 0, None, None)
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#888', -pi/2)
	complex_line['line_r'] = line_r
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#88f', pi/2)
	complex_line['line_l'] = line_l
	for n in range(1, 20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#888', pi/2)
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#88f', pi/2)
		if n == 1:
			line_r['n' + str(n)] = NonrotatedText("i", 20, 50 * n, 0, '#888')
			line_l['n' + str(n)] = NonrotatedText("-i", 20, 50 * n, 20, '#88f')
		else:
			line_r['n' + str(n)] = NonrotatedText(str(n) + "i", 20, 50 * n, 0, '#888')
			line_l['n' + str(n)] = NonrotatedText(str(-n) + "i", 20, 50 * n, 40, '#88f')
	
	group['complex'] = complex_line
	
	await increase_radius(complex_line, scene.scene_height / 2, 2)
	
	await sleep(2.2)
	
	del scene[name]


def create_complex_plane(scene):
	group = Actor(0, 0, '#000', '#000')
	
	group['central_point'] = Circle(2.5, 0, 0, '#000', '#000')
	
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#000', 0)
	group['line_r'] = line_r
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#00f', pi)
	group['line_l'] = line_l
	line_u = Line(scene.scene_width / 2, 1.2, 0, 0, '#888', -pi/2)
	group['line_u'] = line_u
	line_d = Line(scene.scene_width / 2, 1.2, 0, 0, '#88f', pi/2)
	group['line_d'] = line_d
	
	for n in range(20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#000', pi/2)
		line_r['n' + str(n)] = Text(str(n), 20, 50 * n, -25, '#000')
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#00f', pi/2)
		if n > 0:
			line_l['n' + str(n)] = NonrotatedText(str(-n), 20, 50 * n, -25, '#00f')
	
	for n in range(1, 20):
		line_u[str(n)] = Line(10, 1.2, 50 * n, -5, '#888', pi/2)
		line_d[str(n)] = Line(10, 1.2, 50 * n, -5, '#88f', pi/2)
		if n == 1:
			line_u['n' + str(n)] = NonrotatedText("i", 20, 50 * n, 0, '#888')
			line_d['n' + str(n)] = NonrotatedText("-i", 20, 50 * n, 20, '#88f')
		elif n > 1:
			line_u['n' + str(n)] = NonrotatedText(str(n) + "i", 20, 50 * n, 0, '#888')
			line_d['n' + str(n)] = NonrotatedText(str(-n) + "i", 20, 50 * n, 40, '#88f')
	
	return group


async def animate_simple_complex_operations(scene, name='complex_plane'):
	group = Actor(scene.scene_width / 2, scene.scene_height / 2, None, None)
	scene[name] = group
	group['coords'] = create_complex_plane(scene)
	
	await sleep(0.5)
	
	group['info'] = Text("", 40, 45, -95, '#f00')
	
	group['info'].text = "i**2 = -1"
	await fadein(group['info'], 0.3)
	await sleep(2)
	await fadeout(group['info'], 0.3)
	
	group['info'].text = "sqrt(-1) = i"
	await fadein(group['info'], 0.3)
	await sleep(2)
	await fadeout(group['info'], 0.3)
	
	del scene[name]


if __name__ == '__main__':
	from gtk_app import run_animation
	
	scene = Scene(1920, 1080)
	
	background = Actor(0, 0, None, None)
	
	background['layer3'] = Actor(scene.scene_width / 2 + randint(-300, 300), scene.scene_height / 2 + randint(-300, 300), None, None)
	img = Actor(0, 0, None, None)
	background['layer3']['img'] = img
	ifs = []
	for n in range(8):
		ifs.append((randint(-600, 600), randint(-600, 600), 0.5, 0.5, (randbelow(90) / 90) * 2 * pi))
	for n in range(1, 6):
		img[f'f{n}'] = Fractal(ifs, n, 0, 0)
		img[f'f{n}']['c'] = Circle(10, 0, 0, '#fff', None)
	img.cache()
	
	background['layer2'] = Actor(scene.scene_width / 2 + randint(-300, 300), scene.scene_height / 2 + randint(-300, 300), None, None)
	img = Actor(0, 0, None, None)
	background['layer2']['img'] = img
	ifs = []
	for n in range(8):
		ifs.append((randint(-600, 600), randint(-600, 600), 0.5, 0.5, (randbelow(90) / 90) * 2 * pi))
	for n in range(1, 6):
		img[f'f{n}'] = Fractal(ifs, n, 0, 0)
		img[f'f{n}']['c'] = Circle(10, 0, 0, '#bbf', None)
	img.cache()
	
	background['layer1'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/967391.png', scene.scene_width / 2, scene.scene_height / 2, None, None)
	#background['layer3'] = Actor(scene.scene_width / 2, scene.scene_height / 2, None, None)
	img = Actor(0, 0, None, None)
	background['layer1']['img'] = img
	for m in range(6):
		g = Actor(0, 0, None, None, rotate=2 * pi * (randbelow(24) / 24))
		ifs = [(500, 0, 1/2, 1/2, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/3, 1/3, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/4, 1/4, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/5, 1/5, 2 * pi * (randbelow(12) / 12))]
		for n in range(2, 7):
			g[f'f{n}'] = Fractal(ifs, n, 0, 0)
			g[f'f{n}']['c'] = HollowCircle(450 + randbelow(100), 390 + randbelow(50), 0, 0, '#ee4', '#000')
			g[f'f{n}']['l1'] = Line(3000, 0.5, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
			g[f'f{n}']['l1'] = Line(3000, 0.5, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
			g[f'f{n}']['l3'] = Line(3000, 1, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
		img[f'g{m}'] = g	
	img.cache()
	
	scene['bg'] = background
		
	async def animate_background(scene):
		await gather(
			rotate(scene['bg']['layer3'], 2 * pi / 30, 2),
			rotate(scene['bg']['layer2'], -2 * pi / 90, 2),
			rotate(scene['bg']['layer1'], pi / 60, 2),
			translate(scene['bg']['layer3'], randint(-50, 50), randint(-50, 50), 2),
			translate(scene['bg']['layer2'], randint(-50, 50), randint(-50, 50), 2),
			move_bubbles(scene['bg']['layer1'], 2)
		)

	animation = Animation(animate_background)
	
	@animation.take
	async def take0(scene):
		scene['bg'].alpha = 1
		if 'take' in scene: del scene['take']
		await sleep(2)
	
	@animation.take
	async def take1(scene):
		scene['bg'].alpha = 1
		if 'take' in scene: del scene['take']
		await animate_button(scene, 'take')
		await fadeout(background, 1, 0.1)
	
	@animation.take
	async def take2(scene):
		scene['bg'].alpha = 0.1
		if 'take' in scene: del scene['take']
		await sleep(1)
		await animate_complex_plane(scene, 'take')
	
	@animation.take
	async def take3(scene):
		scene['bg'].alpha = 0.1
		if 'take' in scene: del scene['take']
		await animate_simple_complex_operations(scene, 'take')
	
	run_animation(scene, animation)





