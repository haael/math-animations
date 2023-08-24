#!/usr/bin/python3

import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo
import cairo
from math import *
from random import randint


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
	
	def __contains__(self, name):
		return name in self.child
	
	def __getitem__(self, name):
		return self.child[name]
	
	def __setitem__(self, name, actor):
		actor.parent = self
		self.child[name] = actor
	
	def __delitem__(self, name):
		del self.child[name]
	
	def render(self, ctx, alpha=1):
		if hasattr(self, 'cached'):
			ctx.set_source_surface(self.cached, -1500, -1500)
			#ctx.translate(1000, 1000)
			ctx.paint_with_alpha(alpha)
			return
		
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
		
		for key in sorted(self.child.keys()):
			item = self.child[key]
			
			if self.alpha * alpha < 1:
				ctx.push_group()
			else:
				ctx.save()
			
			item.render(ctx)
			
			if self.alpha * alpha < 1:
				ctx.pop_group_to_source()
				ctx.paint_with_alpha(self.alpha * alpha)
			else:
				ctx.restore()
		
		ctx.restore()
	
	def cache(self):
		cached = cairo.ImageSurface(cairo.Format.ARGB32, 3000, 3000)
		#cached = cairo.RecordingSurface(cairo.Content.COLOR_ALPHA, None)
		ctx = cairo.Context(cached)
		ctx.translate(1500, 1500)
		self.render(ctx)
		#cached.finish()
		self.cached = cached


class Scene(Actor):
	def __init__(self, scene_width, scene_height, cx=0, cy=0):
		self.scene_width = scene_width
		self.scene_height = scene_height
		super().__init__(scene_width * cx, scene_height * cy, None, None)


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
		
		ctx.clip()
		
		super().render(ctx, alpha)


class HollowCircle(Actor):
	def __init__(self, outer_radius, inner_radius, x, y, fill, stroke, **kwargs):
		super().__init__(x, y, fill, stroke, **kwargs)
		self.outer_radius = outer_radius
		self.inner_radius = inner_radius
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		ctx.set_fill_rule(cairo.FillRule.EVEN_ODD)
		ctx.arc(self.x, self.y, self.outer_radius, 0, 2 * pi)
		#ctx.close_path()
		ctx.arc(self.x, self.y, self.inner_radius, 0, 2 * pi)
		#ctx.clip()
		
		if any(self.fill):
			ctx.set_source_rgba(*self.fill[:3], self.fill[3] * self.alpha * alpha)
			ctx.fill_preserve()
		
		if any(self.stroke):
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			ctx.stroke_preserve()
		
		ctx.clip()
		
		super().render(ctx, alpha)


class Line(Actor):
	def __init__(self, length, width, x, y, color, rotate, **kwargs):
		super().__init__(x, y, None, color, rotate=rotate, **kwargs)
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
	def __init__(self, text, size, x, y, color, **kwargs):
		super().__init__(x, y, color, color, **kwargs)
		self.text = text
		self.size = size
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		if any(self.fill):

			## Next four lines take care of centering the text. Feel free to ignore ;-)
			#width, height = surface.get_width(), surface.get_height()
			#print(width, height)
			#w, h = layout.get_pixel_size()
			#position = (width/2.0 - w/2.0, height/2.0 - h/2.0)
			#position = (w,h)
			#context.move_to(*position)
			
			ctx.move_to(self.x, self.y)
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			
			layout = PangoCairo.create_layout(ctx)
			layout.set_font_description(Pango.FontDescription(f'Monospace {self.size}px'))
			layout.set_text(self.text, -1);
			PangoCairo.show_layout(ctx, layout)
		
		ctx.new_path()
		
		super().render(ctx, alpha)


class NonrotatedText(Actor):
	def __init__(self, text, size, x, y, color, **kwargs):
		super().__init__(x, y, color, color, **kwargs)
		self.text = text
		self.size = size
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		if any(self.fill):
			unrotate = self.rotate
			actor = self
			while hasattr(actor, 'parent'):
				actor = actor.parent
				unrotate += actor.rotate
			
			ctx.translate(self.x, self.y + self.size / 2)
			ctx.rotate(-unrotate)
			ctx.translate(-self.x, -self.y - self.size / 2)
			
			ctx.move_to(self.x, self.y)
			#ctx.set_font_size(self.size)
			#ctx.text_path(self.text)
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			#ctx.fill()
			
			layout = PangoCairo.create_layout(ctx)
			layout.set_font_description(Pango.FontDescription(f'Monospace {self.size}px'))
			layout.set_text(self.text, -1);
			PangoCairo.show_layout(ctx, layout)
		
		super().render(ctx, alpha)


class Bubbles(Actor):
	@classmethod
	def random(cls, extent, background, x, y, fill, stroke, **kwargs):
		bubbles = []
		l = randint(10, 20)
		for n in range(l):
			bubbles.append([randint(0, extent) - randint(0, extent), randint(0, extent) - randint(0, extent), randint(extent / 10, extent / 3)])
		return cls(bubbles, background, x, y, fill, stroke, **kwargs)
	
	def __init__(self, bubbles, background, x, y, fill, stroke, **kwargs):
		super().__init__(x, y, fill, stroke, **kwargs)
		self.bubbles = bubbles
		if background is not None:
			self.background = cairo.ImageSurface.create_from_png(background)
		else:
			self.background = None
	
	def render(self, ctx, alpha=1):
		if alpha <= 0: return
		
		if self.background is not None:
			ctx.save()
			#ctx.translate(self.x, self.y)
			#ctx.rotate(self.rotate)
			#ctx.translate(-self.x, -self.y)
			#ctx.scale(3, 3)
			ctx.identity_matrix()
			ctx.set_source_surface(self.background)
			ctx.paint_with_alpha(self.alpha * alpha)
			ctx.restore()
		
		for x, y, radius in self.bubbles:
			ctx.arc(self.x + x * cos(self.rotate) + y * sin(self.rotate), self.y - x * sin(self.rotate) + y * cos(self.rotate), radius, 0, 2 * pi)
			ctx.close_path()
		
		if any(self.fill):
			ctx.set_source_rgba(*self.fill[:3], self.fill[3] * self.alpha * alpha)
			ctx.fill_preserve()
		
		if any(self.stroke):
			ctx.set_source_rgba(*self.stroke[:3], self.stroke[3] * self.alpha * alpha)
			ctx.stroke_preserve()
		
		#ctx.new_path()
		
		#for x, y, radius in self.bubbles:
		#	ctx.arc(self.x + x * cos(self.rotate) + y * sin(self.rotate), self.y - x * sin(self.rotate) + y * cos(self.rotate), radius, 0, 2 * pi)
		ctx.clip()
		
		super().render(ctx, alpha)


class Fractal(Actor):
	def __init__(self, ifs, levels, x, y, **kwargs):
		super().__init__(x, y, None, None, **kwargs)
		self.ifs = ifs
		self.levels = levels
	
	def render(self, ctx, alpha=1, level=0):
		if alpha <= 0: return
		
		if level < self.levels:
			for tx, ty, sx, sy, r in self.ifs:
				ctx.save()
				ctx.translate(tx, ty)
				
				ctx.translate(self.x, self.y)
				ctx.scale(sx, sy)
				ctx.rotate(r)
				ctx.translate(-self.x, -self.y)

				self.render(ctx, alpha, level + 1)
				ctx.restore()
		else:
			super().render(ctx, alpha)


