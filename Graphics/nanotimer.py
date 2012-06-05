#!/usr/bin/python

from __future__ import division

import time
import math
import pyglet
from pyglet.gl import *


fps = pyglet.clock.ClockDisplay()
clock = pyglet.clock.get_default()
class GridWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(GridWindow, self).__init__(*args, **kwargs)

		self.arial = pyglet.font.load('Arial', 60, bold=True)

		clock.schedule_interval(self.animate, 1.0/240.0)


	def animate(self, dt):
		return

	def on_resize(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1.0, 2.0)
		glMatrixMode(GL_MODELVIEW)

		glClearColor(0.4, 0.4, 0.4, 1.0)

		#glEnable(GL_MULTISAMPLE)
		glEnable(GL_DEPTH_TEST)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glEnable(GL_POLYGON_SMOOTH)
		glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

		return pyglet.event.EVENT_HANDLED


	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		w,h = self.get_size()

		cx = w / 2
		cy = h / 2

		tstr = "%.20f" % time.time()
		text = pyglet.font.Text(self.arial, tstr, x=cx, y=cy, halign='center', valign='center', color=(0.6,0.6,0.6,1))
		text.draw()

		glDisable(GL_DEPTH_TEST)
		fps.draw()
		glEnable(GL_DEPTH_TEST)


def triVerts(x, y, z, sz, rot):
	return (x + sz/2 * math.cos(rot),               y + sz/2 * math.sin(rot),               z,
	        x + sz/2 * math.cos(rot + 2.1*math.pi/3), y + sz/2 * math.sin(rot + 2.1*math.pi/3), z,
	        x + sz/2 * math.cos(rot - 2.1*math.pi/3), y + sz/2 * math.sin(rot - 2.1*math.pi/3), z)


if __name__ == '__main__':
	try:
		config = pyglet.gl.Config(depth_size=24, double_buffer=True, sample_buffers=1, samples=4)
		window = GridWindow(resizable=True, config=config)
	except pyglet.window.NoSuchConfigException:
		window = GridWindow(resizable=True)

	pyglet.app.run()
