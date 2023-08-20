#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
from signal import signal, SIGTERM
from math import *
from asyncio import run, set_event_loop_policy, sleep, gather
from asyncio_glib import GLibEventLoopPolicy


set_event_loop_policy(GLibEventLoopPolicy())


viewport_width = viewport_height = 0
scene_width = 1920
scene_height = 1080


def color(s):
	if s[0] != '#':
		raise ValueError
	elif len(s) == 3 + 1:
		r = int(s[1:2], 16) / 15
		g = int(s[2:3], 16) / 15
		b = int(s[3:4], 16) / 15
		a = 1
	elif len(s) == 4 + 1:
		r = int(s[1:2], 16) / 15
		g = int(s[2:3], 16) / 15
		b = int(s[3:4], 16) / 15
		a = int(s[4:5], 16) / 15
	elif len(s) == 6 + 1:
		r = int(s[1:3], 16) / 255
		g = int(s[3:5], 16) / 255
		b = int(s[5:7], 16) / 255
		a = 1
	elif len(s) == 8 + 1:
		r = int(s[1:3], 16) / 255
		g = int(s[3:5], 16) / 255
		b = int(s[5:7], 16) / 255
		a = int(s[7:9], 16) / 255
	else:
		raise ValueError
	
	return r, g, b, a


class Actor:
	def __init__(self, x, y, fill, stroke, alpha=1, scale=(1, 1), rotate=0):
		self.x = x
		self.y = y
		if isinstance(fill, str): fill = color(fill)
		if isinstance(stroke, str): stroke = color(stroke)
		if fill is None: fill = 0, 0, 0, 0
		if stroke is None: stroke = 0, 0, 0, 0
		self.fill = list(fill)
		self.stroke = list(stroke)
		self.alpha = alpha
		self.scale = list(scale)
		self.rotate = rotate
		self.child = {}
	
	def __getitem__(self, name):
		return self.child[name]
	
	def __setitem__(self, name, actor):
		self.child[name] = actor
	
	def __delitem__(self, n):
		del self.child[name]
	
	def render(self, ctx, alpha=1):
		ctx.save()
		
		ctx.translate(self.x, self.y)
		
		try:
			scale_x, scale_y = self.scale
			ctx.scale(scale_x, scale_y)
		except TypeError:
			if any(_x != 1 for _x in self.scale):
				ctx.scale(self.scale[0], self.scale[0])
		
		if self.rotate:
			ctx.rotate(self.rotate)
		
		for item in self.child.values():
			item.render(ctx, self.alpha * alpha)
		
		ctx.restore()


class Circle(Actor):
	def __init__(self, radius, x, y, fill, stroke, **kwargs):
		super().__init__(x, y, fill, stroke, **kwargs)
		self.radius = radius
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		ctx.arc(self.x, self.y, self.radius, 0, 2 * pi)
		
		if any(self.fill):
			ctx.set_source_rgba(*self.fill[:3], self.fill[3] * self.alpha * alpha)
			ctx.fill_preserve()
		
		if any(self.stroke):
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			ctx.stroke_preserve()
		
		ctx.new_path()
		
		super().render(ctx, alpha)


class Line(Actor):
	def __init__(self, length, width, x, y, fill, stroke, **kwargs):
		super().__init__(x, y, fill, stroke, **kwargs)
		self.length = length
		self.width = width
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		if any(self.stroke):
			ctx.set_line_width(self.width)
			ctx.move_to(self.x, self.y)
			ctx.line_to(self.x + self.length * cos(self.rotate), self.y + self.length * sin(self.rotate))
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			ctx.stroke()
		
		ctx.new_path()
		
		super().render(ctx, alpha)


class Text(Actor):
	def __init__(self, text, size, x, y, fill, stroke, **kwargs):
		super().__init__(x, y, fill, stroke, **kwargs)
		self.text = text
		self.size = size
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		if any(self.fill):
			ctx.move_to(self.x, self.y)
			ctx.set_font_size(self.size)
			ctx.text_path(self.text)
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			ctx.fill()
		
		ctx.new_path()
		
		super().render(ctx, alpha)




scene = Actor(scene_width / 2, scene_height / 2, None, None)


async def fadein(actor, duration):
	steps = ceil(25 * duration)
	for n in range(steps):
		actor.alpha = n**2 / steps**2
		await sleep(1 / 25)
	
	actor.alpha = 1


async def fadeout(actor, duration):
	steps = ceil(25 * duration)
	for n in range(steps):
		actor.alpha = (steps - n - 1)**2 / steps**2
		await sleep(1 / 25)
	
	actor.alpha = 0


async def translate(actor, tx, ty, duration):
	bx = actor.x
	by = actor.y
	steps = ceil(25 * duration)
	for n in range(steps):
		actor.x = bx + tx * n / steps
		actor.y = by + ty * n / steps
		await sleep(1 / 25)
	
	actor.x = bx + tx
	actor.y = by + ty


async def rotate(actor, angle, duration):
	start = actor.rotate
	steps = ceil(25 * duration)
	for n in range(0, steps):
		actor.rotate = start + angle * n / steps
		await sleep(1 / 25)
	
	actor.rotate = start + angle


async def animate_button():
	global scene
	
	scene = Circle(100, scene_width / 2, 0, '#800', '#f0f', alpha=0)
	await sleep(0.5)
	
	await gather(
		translate(scene, 0, scene_height / 2, 1.5),
		fadein(scene, 1.5)
	)
	
	scene['one'] = Circle(10, 0, 20, '#0f0', '#0ff', alpha=0)
	scene['two'] = Circle(10, 0, -20, '#0f0', '#0ff', alpha=0)
	scene['three'] = Circle(10, 20, 0, '#0f0', '#0ff', alpha=0)
	scene['four'] = Circle(10, -20, 0, '#f00', '#f00', alpha=0)
	
	await gather(
		fadein(scene['one'], 0.5),
		fadein(scene['two'], 1),
		fadein(scene['three'], 1.5),
		fadein(scene['four'], 2)
	)
	await rotate(scene, pi / 2, 1)
	await sleep(1)
	await fadeout(scene, 1.5)
	await sleep(1)


async def animate_number_line():
	global scene
	
	scene = Actor(scene_width / 2, scene_height / 2, '#000', '#000')
	line_r = Line(scene_width / 2, 1.2, 0, 0, '#000', '#000')
	scene['line_r'] = line_r
	await sleep(1.2)
	
	for n in range(20):
		line_r[str(n)] = Line(10, 1.2, 50 * n, -5, '#000', '#000', rotate=pi/2)
		line_r['n' + str(n)] = Text(str(n), 20, 50 * n, -10, '#000', '#000')
		await sleep(0.05)
	await sleep(1.2)


async def animate():
	await animate_button()
	await animate_number_line()
	window.close()


def draw(widget, ctx):
	scale = min(viewport_width / scene_width, viewport_height / scene_height)
	if not scale: return
	
	ctx.set_source_rgb(0, 0, 0)
	ctx.paint()
	
	ctx.translate((viewport_width - scene_width * scale) / 2, (viewport_height - scene_height * scale) / 2)
	ctx.scale(scale, scale)
	ctx.rectangle(0, 0, scene_width, scene_height)
	ctx.clip()
	ctx.set_source_rgb(1, 1, 1)
	ctx.paint()
	
	scene.render(ctx)


def key_release_event(widget, event):
	if Gdk.keyval_name(event.keyval) == 'Escape':
		window.close()


def configure_event(widget, event):
	global viewport_width, viewport_height
	viewport_width = event.width
	viewport_height = event.height


mainloop = GLib.MainLoop()

window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
widget = Gtk.DrawingArea()
window.add(widget)
window.show_all()

widget.connect('configure-event', configure_event)
widget.connect('draw', draw)
window.connect('key-release-event', key_release_event)
window.connect('destroy', lambda window: mainloop.quit())
signal(SIGTERM, lambda signum, frame: mainloop.quit())


GLib.idle_add(lambda: run(animate()))

def redraw():
	widget.queue_draw()
	return True

GLib.timeout_add(25, redraw)

try:
	mainloop.run()
except KeyboardInterrupt:
	print()

