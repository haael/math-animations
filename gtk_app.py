#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
from signal import signal, SIGTERM
from math import *
from asyncio import run, set_event_loop_policy, sleep, gather
from asyncio_glib import GLibEventLoopPolicy


def draw(widget, ctx):
	scene = widget.scene
	
	scale = min(widget.viewport_width / scene.scene_width, widget.viewport_height / scene.scene_height)
	if not scale: return
	
	ctx.set_source_rgb(0, 0, 0)
	ctx.paint()
	
	ctx.translate((widget.viewport_width - scene.scene_width * scale) / 2, (widget.viewport_height - scene.scene_height * scale) / 2)
	ctx.scale(scale, scale)
	ctx.rectangle(0, 0, scene.scene_width, scene.scene_height)
	ctx.clip()
	ctx.set_source_rgb(1, 1, 1)
	ctx.paint()
	
	scene.render(ctx)


def key_release_event(widget, event):
	if Gdk.keyval_name(event.keyval) == 'Escape':
		widget.close()


def configure_event(widget, event):
	widget.viewport_width = event.width
	widget.viewport_height = event.height


def tick_callback(widget, frame):
	widget.queue_draw()
	return True


def run_animation(scene, animation):
	mainloop = GLib.MainLoop()
	set_event_loop_policy(GLibEventLoopPolicy())
	
	window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
	widget = Gtk.DrawingArea()
	widget.scene = scene
	widget.add_tick_callback(tick_callback)
	window.add(widget)
	window.show_all()
	window.fullscreen()
	
	#def realize_event(widget):
	#	widget.get_window().set_cursor(Gdk.BLANK_CURSOR)
	#widget.connect('realize', realize_event)
	
	widget.connect('configure-event', configure_event)
	widget.connect('draw', draw)
	window.connect('key-release-event', key_release_event)
	widget.connect('destroy', lambda window: mainloop.quit())
	
	signal(SIGTERM, lambda signum, frame: mainloop.quit())	
	
	GLib.idle_add(lambda: run(animation))
	
	try:
		mainloop.run()
	except KeyboardInterrupt:
		print()





