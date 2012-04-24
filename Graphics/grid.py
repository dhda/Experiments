#!/usr/bin/python

from __future__ import division

import math
import pyglet
from pyglet.gl import *


fps = pyglet.clock.ClockDisplay()
class GridWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(GridWindow, self).__init__(*args, **kwargs)

		self.box_color  = (0.9, 0.9, 0.9)
		self.line_color = (0.7, 0.7, 0.7)

		self.box_w = 20
		self.box_h = 20
		self.n_boxes = 1

		self.top = 0

		self.batch = pyglet.graphics.Batch()
		self.quads = self.batch.add(1, pyglet.gl.GL_QUADS, None, 'v3f', 'c3f')
		self.lines = self.batch.add(1, pyglet.gl.GL_LINES, None, 'v3f', 'c3f')

		self.animating = dict()

		pyglet.clock.schedule_interval(self.animate, 1.0/120.0)


	def on_mouse_motion(self, x, y, dx, dy):
		w,h = self.get_size()

		c = min(self.x_boxes-1, x // self.box_w)
		r = min(self.y_boxes-1, y // self.box_h)

		i = c + r*self.x_boxes

		self.top += 1
		self.animating[i] = [1.0, self.top, dx, dy]


	def animate(self, dt):
		for i in self.animating.keys():
			p = max(0, self.animating[i][0])
			if p != 0:
				d = self.animating[i][1] / self.top
			else:
				d = 0

			c = i %  self.x_boxes
			r = i // self.x_boxes

			e = p**3
			z = max(0, self.box_w/2.0 * e)

			cr = cg = min(1.0, e / self.box_w * math.sqrt(self.animating[i][2]**2 + self.animating[i][3]**2))

			self.quads.colors[12*i : 12*i+12] = [self.box_color[0]*(1.0-cr), self.box_color[1]*(1.0-cg), self.box_color[2]]*4
			self.quads.vertices[12*i : 12*i+12] = [c*self.box_w-z,     r*self.box_h-z,     d,
			                                       (c+1)*self.box_w+z, r*self.box_h-z,     d,
			                                       (c+1)*self.box_w+z, (r+1)*self.box_h+z, d,
			                                       c*self.box_w-z,     (r+1)*self.box_h+z, d]
			
			self.lines.colors[24*i : 24*i+24] = [self.line_color[0]*(1.0-0.3*e), self.line_color[1]*(1.0-0.3*e), self.line_color[2]*(1.0-0.3*e)]*8

			self.lines.vertices[24*i    : 24*i+3]  = self.quads.vertices[12*i   : 12*i+3]
			self.lines.vertices[24*i+3  : 24*i+6]  = self.quads.vertices[12*i+3 : 12*i+6]
                                                                                         
			self.lines.vertices[24*i+6  : 24*i+9]  = self.quads.vertices[12*i+3 : 12*i+6]
			self.lines.vertices[24*i+9  : 24*i+12] = self.quads.vertices[12*i+6 : 12*i+9]
                                                                                         
			self.lines.vertices[24*i+12 : 24*i+15] = self.quads.vertices[12*i+6 : 12*i+9]
			self.lines.vertices[24*i+15 : 24*i+18] = self.quads.vertices[12*i+9 : 12*i+12]
                                                                                         
			self.lines.vertices[24*i+18 : 24*i+21] = self.quads.vertices[12*i+9 : 12*i+12]
			self.lines.vertices[24*i+21 : 24*i+24] = self.quads.vertices[12*i   : 12*i+3]

			if p == 0:
				del self.animating[i]
				pass
			else:
				self.animating[i][0] = p - 2.5*dt

		if len(self.animating) == 0:
			self.top = 0


	def on_resize(self, width, height):
		#super(GridWindow, self).on_resize(width, height)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1.0, 2.0)
		glMatrixMode(GL_MODELVIEW)

		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)

		x_boxes = max(1, width  // self.box_w) + 1
		y_boxes = max(1, height // self.box_h) + 1
		n_boxes = x_boxes * y_boxes

		if n_boxes == self.n_boxes:
			return
		else:
			self.x_boxes = x_boxes
			self.y_boxes = y_boxes
			self.n_boxes = n_boxes


		self.animating = dict()

		self.quads.resize(4 * n_boxes)
		self.lines.resize(8 * n_boxes)

		for i in xrange(n_boxes):
			c = i %  x_boxes
			r = i // x_boxes

			self.quads.vertices[12*i : 12*i+12] = [c*self.box_w,     r*self.box_h,     0.0,
			                                       (c+1)*self.box_w, r*self.box_h,     0.0,
			                                       (c+1)*self.box_w, (r+1)*self.box_h, 0.0,
			                                       c*self.box_w,     (r+1)*self.box_h, 0.0]

			self.lines.vertices[24*i    : 24*i+3]  = self.quads.vertices[12*i   : 12*i+3]
			self.lines.vertices[24*i+3  : 24*i+6]  = self.quads.vertices[12*i+3 : 12*i+6]
                                                                                         
			self.lines.vertices[24*i+6  : 24*i+9]  = self.quads.vertices[12*i+3 : 12*i+6]
			self.lines.vertices[24*i+9  : 24*i+12] = self.quads.vertices[12*i+6 : 12*i+9]
                                                                                         
			self.lines.vertices[24*i+12 : 24*i+15] = self.quads.vertices[12*i+6 : 12*i+9]
			self.lines.vertices[24*i+15 : 24*i+18] = self.quads.vertices[12*i+9 : 12*i+12]
                                                                                         
			self.lines.vertices[24*i+18 : 24*i+21] = self.quads.vertices[12*i+9 : 12*i+12]
			self.lines.vertices[24*i+21 : 24*i+24] = self.quads.vertices[12*i   : 12*i+3]


			self.quads.colors[12*i : 12*i+12] = [self.box_color[0], self.box_color[1], self.box_color[2]]*4
			self.lines.colors[24*i : 24*i+24] = [self.line_color[0], self.line_color[1], self.line_color[2]]*8


	def on_draw(self):
		self.clear()

		"""
		w,h = self.get_size()
		aspect = w/h
		fov = 80.0
		near = 1.0
		far = 1000.0
		bt = math.tan(math.radians(fov/2.0))
		lr = bt * aspect

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glFrustum(-lr*near, lr*near, -bt*near, bt*near, near, far)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		#glTranslatef(-w/2.0+0.5, -h/2.0+0.5, -h/bt/2.0)
		"""

		glPushMatrix()
		glTranslatef(0.5, 0.5, 0.0)

		glEnable(GL_MULTISAMPLE_ARB)

		self.batch.draw()

		glPopMatrix()

		glDisable(GL_DEPTH_TEST)
		fps.draw()
		glEnable(GL_DEPTH_TEST)


if __name__ == '__main__':
	config = pyglet.gl.Config(depth_size=24, double_buffer=True, sample_buffers=1, samples=4)
	window = GridWindow(config=config, resizable=True)
	pyglet.app.run()
