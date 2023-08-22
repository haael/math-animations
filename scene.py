#!/usr/bin/python3


import cairo
from math import *
from asyncio import run, set_event_loop_policy, sleep, gather

from shapes import *
from animations import *


async def animate_button(scene):
	rr = randbelow(1000000)
	group = Circle(100, scene.scene_width / 2, 0, '#800', '#f0f', alpha=0)
	scene[f'animate_button_{rr}'] = group
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
	del scene[f'animate_button_{rr}']


async def animate_complex_plane(scene):
	rr = randbelow(1000000)
	group = Actor(scene.scene_width / 2, scene.scene_height / 2, '#000', '#000')
	scene[f'animate_complex_plane_{rr}'] = group
	
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
	
	del scene[f'animate_complex_plane_{rr}']


def create_complex_plane(scene):
	group = Actor(scene.scene_width / 2, scene.scene_height / 2, '#000', '#000')
	
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


async def animate_simple_complex_operations(scene):
	rr = randbelow(1000000)
	scene[f'complex_plane_{rr}'] = create_complex_plane(scene)
	
	await sleep(0.5)
	
	scene['info'] = Text("", 40, scene.scene_width / 2 + 45, scene.scene_height / 2 - 95, '#f00')
	
	scene['info'].text = "i**2 = -1"
	await fadein(scene['info'], 0.3)
	await sleep(2)
	await fadeout(scene['info'], 0.3)
	
	scene['info'].text = "sqrt(-1) = i"
	await fadein(scene['info'], 0.3)
	await sleep(2)
	await fadeout(scene['info'], 0.3)
	
	del scene['info']
	
	del scene[f'complex_plane_{rr}']





if __name__ == '__main__':
	from gtk_app import run_animation
	
	scene = Scene(1920, 1080)
		
	
	async def animate(scene):
		fg_running = True
		
		background = Actor(0, 0, None, None)
		gk = Actor(0, 0, None, None)
		ifs = []
		for n in range(8):
			ifs.append((randint(-600, 600), randint(-600, 600), 0.5, 0.5, (randbelow(90) / 90) * 2 * pi))
		for n in range(1, 6):
			gk[f'f{n}'] = Fractal(ifs, n, 0, 0)
			gk[f'f{n}']['c'] = Circle(10, 0, 0, '#000', None)
		gg = Actor(scene.scene_width / 2 + randint(-300, 300), scene.scene_height / 2 + randint(-300, 300), None, None)
		background['gg1'] = gg
		background['gg1']['gk'] = gk
		gk.cache()
		
		gk = Actor(0, 0, None, None)
		ifs = []
		for n in range(8):
			ifs.append((randint(-600, 600), randint(-600, 600), 0.5, 0.5, (randbelow(90) / 90) * 2 * pi))
		for n in range(1, 6):
			gk[f'f{n}'] = Fractal(ifs, n, 0, 0)
			gk[f'f{n}']['c'] = Circle(10, 0, 0, '#00f', None)
		gg = Actor(scene.scene_width / 2 + randint(-300, 300), scene.scene_height / 2 + randint(-300, 300), None, None)
		background['gg2'] = gg
		background['gg2']['gk'] = gk
		gk.cache()
		
		gk = Actor(0, 0, None, None)
		for m in range(6):
			g = Actor(0, 0, None, None, rotate=2 * pi * (randbelow(24) / 24))
			ifs = [(500, 0, 1/2, 1/2, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/3, 1/3, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/4, 1/4, 2 * pi * (randbelow(12) / 12)), (500, 0, 1/5, 1/5, 2 * pi * (randbelow(12) / 12))]
			for n in range(2, 7):
				g[f'f{n}'] = Fractal(ifs, n, 0, 0)
				g[f'f{n}']['c'] = HollowCircle(450 + randbelow(100), 390 + randbelow(50), 0, 0, '#ee4', '#000')
				g[f'f{n}']['l1'] = Line(3000, 0.5, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
				g[f'f{n}']['l1'] = Line(3000, 0.5, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
				g[f'f{n}']['l3'] = Line(3000, 1, 0, 0, '#000', 2 * pi * (randbelow(36) / 36))
			gk[f'g{m}'] = g	
		gg = Actor(scene.scene_width / 2, scene.scene_height / 2, None, None)
		background['gg3'] = gg
		background['gg3']['gk'] = gk
		gk.cache()
		
		scene['bg'] = background
		
		async def animate_bg():
			nonlocal fg_running
			while fg_running:
				await gather(
					rotate(scene['bg']['gg1'], 2 * pi / 30, 2),
					rotate(scene['bg']['gg2'], -2 * pi / 90, 2),
					rotate(scene['bg']['gg3'], pi / 60, 2),
					translate(scene['bg']['gg1'], randint(-50, 50), randint(-50, 50), 2),
					translate(scene['bg']['gg2'], randint(-50, 50), randint(-50, 50), 2)
				)
		
		#scene['1'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/967391.png', scene.scene_width / 2, scene.scene_height / 2, None, None, alpha=0.025)
		#scene['1']['2'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/470563.png', 0, 0, None, None)
		#scene['1']['2']['3'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/878415.png', 0, 0, None, None)
		#scene['4'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/894423.png', scene.scene_width / 2, scene.scene_height / 2, None, None, alpha=0.025)
		#scene['4']['5'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/876443.png', 0, 0, None, None)
		#scene['4']['5']['6'] = Bubbles.random(scene.scene_width / 2,  '/home/haael/Pobrane/fractals/876859.png', 0, 0, None, None)
		
		
		#async def animate_bg():
		#	nonlocal fg_running
		#	while fg_running:
		#		await gather(
		#			rotate(scene['1'], pi / 10, 2),
		#			move_bubbles(scene['1'], 2),
		#			move_bubbles(scene['1']['2'], 2),
		#			move_bubbles(scene['1']['2']['3'], 2),
		#			rotate(scene['4'], -pi / 10, 2),
		#			move_bubbles(scene['4'], 2),
		#			move_bubbles(scene['4']['5'], 2),
		#			move_bubbles(scene['4']['5']['6'], 2)
		#		)
		
		async def animate_fg():
			nonlocal fg_running
			await sleep(5)
			await animate_button(scene)
			await fadeout(background, 1, 0.10)
			await sleep(1)
			await animate_complex_plane(scene)
			await animate_simple_complex_operations(scene)
			fg_running = False
		
		await gather(animate_bg(), animate_fg())
		
		#del scene['1']
		#del scene['4']
	
	run_animation(scene, animate(scene))





