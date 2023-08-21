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
	
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#000', '#000')
	group['line_r'] = line_r
	await sleep(1.2)
	
	for n in range(20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#000', '#000', rotate=pi/2)
		line_r['n' + str(n)] = Text(str(n), 20, 50 * n, -25, '#000')
		await sleep(0.05)
	await sleep(1.2)
	
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#00f', '#00f')
	neg_numbers = Actor(0, 0, None, None, alpha=0)
	for n in range(20):
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#00f', '#00f', rotate=pi/2)
		if n > 0:
			neg_numbers['n' + str(n)] = NonrotatedText(str(-n), 20, 50 * n, -25, '#00f')
	line_l['neg_numbers'] = neg_numbers
	group['line_l'] = line_l
	
	await gather(fadein(neg_numbers, 1.5), rotate(line_l, -pi, 1.5))
	await sleep(2)
	
	complex_line = Circle(0, 0, 0, None, None)
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#888', '#888', rotate=-pi/2)
	complex_line['line_r'] = line_r
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#88f', '#88f', rotate=pi/2)
	complex_line['line_l'] = line_l
	for n in range(1, 20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#888', '#888', rotate=pi/2)
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#88f', '#88f', rotate=pi/2)
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
	
	line_r = Line(scene.scene_width / 2, 1.2, 0, 0, '#000', '#000')
	group['line_r'] = line_r
	line_l = Line(scene.scene_width / 2, 1.2, 0, 0, '#00f', '#00f', rotate=pi)
	group['line_l'] = line_l
	line_u = Line(scene.scene_width / 2, 1.2, 0, 0, '#888', '#888', rotate=-pi/2)
	group['line_u'] = line_u
	line_d = Line(scene.scene_width / 2, 1.2, 0, 0, '#88f', '#88f', rotate=pi/2)
	group['line_d'] = line_d
	
	for n in range(20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#000', '#000', rotate=pi/2)
		line_r['n' + str(n)] = Text(str(n), 20, 50 * n, -25, '#000')
		line_l[str(n)] = Line(10, 1.2, 50 * n, -5, '#00f', '#00f', rotate=pi/2)
		if n > 0:
			line_l['n' + str(n)] = NonrotatedText(str(-n), 20, 50 * n, -25, '#00f')
	
	for n in range(1, 20):
		line_u[str(n)] = Line(10, 1.2, 50 * n, -5, '#888', '#888', rotate=pi/2)
		line_d[str(n)] = Line(10, 1.2, 50 * n, -5, '#88f', '#88f', rotate=pi/2)
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
	
	#scene['f1'] = Fractal([(150, 0, 0.5, 0.5, 0), (-150, 0, 0.5, 0.5, 0), (0, 200, 0.33, 0.33, pi/4.5), (0, -200, 0.33, 0.33, pi/3)], 8, scene.scene_width / 2, scene.scene_height / 2)
	#scene['f1']['1'] = Circle(300, 0, 0, '#f00', None)
	
	#scene['f2'] = Fractal([(150, 0, 0.5, 0.5, 0), (-150, 0, 0.5, 0.5, 0), (0, 200, 0.33, 0.33, pi/3.5), (0, -200, 0.33, 0.33, pi/3)], 8, scene.scene_width / 2, scene.scene_height / 2)
	#scene['f1']['2'] = Line(300, 5, 0, 0, None, '#0f0')
	
	#for n in range(15):
	#	scene[f'f{n}'] = Fractal([(5, 0, 0.8, 0.8, pi/50)], n, scene.scene_width / 2, scene.scene_height / 2)
	#	scene[f'f{n}']['c'] = Circle(75, 0, 0, ((15 - n)**2 / 15**2, 0.5, 0.5, 1), None)
	
	#async def animate(scene):
	#	pass
	
	async def animate(scene):
		scene['1'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/967391.png', scene.scene_width / 2, scene.scene_height / 2, None, None, alpha=0.025)
		scene['1']['2'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/470563.png', 0, 0, None, None)
		scene['1']['2']['3'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/878415.png', 0, 0, None, None)
		scene['4'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/894423.png', scene.scene_width / 2, scene.scene_height / 2, None, None, alpha=0.025)
		scene['4']['5'] = Bubbles.random(scene.scene_width / 2, '/home/haael/Pobrane/fractals/876443.png', 0, 0, None, None)
		scene['4']['5']['6'] = Bubbles.random(scene.scene_width / 2,  '/home/haael/Pobrane/fractals/876859.png', 0, 0, None, None)
		
		fg_running = True
		
		async def animate_bg():
			nonlocal fg_running
			while fg_running:
				await gather(
					rotate(scene['1'], pi / 10, 2),
					move_bubbles(scene['1'], 2),
					move_bubbles(scene['1']['2'], 2),
					move_bubbles(scene['1']['2']['3'], 2),
					rotate(scene['4'], -pi / 10, 2),
					move_bubbles(scene['4'], 2),
					move_bubbles(scene['4']['5'], 2),
					move_bubbles(scene['4']['5']['6'], 2)
				)
		
		async def animate_fg():
			nonlocal fg_running
			await animate_button(scene)
			await animate_complex_plane(scene)
			await animate_simple_complex_operations(scene)
			fg_running = False
		
		await gather(animate_bg(), animate_fg())
		
		#del scene['1']
		#del scene['4']
	
	run_animation(scene, animate(scene))





