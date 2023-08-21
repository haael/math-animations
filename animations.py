#!/usr/bin/python3

from math import *
from random import randint
from asyncio import run, set_event_loop_policy, sleep, gather


def randbelow(n):
	return randint(0, n - 1)


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


async def increase_radius(actor, radius, duration):
	start = actor.radius
	steps = ceil(25 * duration)
	for n in range(0, steps):
		actor.radius = start + (radius - start) * n / steps
		await sleep(1 / 25)
	
	actor.radius = radius


async def move_bubbles(actor, duration):
	dirs = []
	for n in range(len(actor.bubbles)):
		dirs.append([randint(-100, 100), randint(-100, 100)])
	
	steps = ceil(25 * duration)
	for m in range(steps):
		for n, (tx, ty) in enumerate(dirs):
			actor.bubbles[n][0] += tx / steps
			actor.bubbles[n][1] += ty / steps
		await sleep(1 / 25)
	
	for n, (tx, ty) in enumerate(dirs):
		actor.bubbles[n][0] += 1 / steps
		actor.bubbles[n][1] += 1 / steps


