#!/usr/bin/python

from __future__ import division

import pyglet


fps = pyglet.clock.ClockDisplay()
class GridWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super(GridWindow, self).__init__(*args, **kwargs)

		self.box_color  = (0.9, 0.9, 0.9)
		self.line_color = (0.8, 0.8, 0.8)

		self.box_w = 20
		self.box_h = 20
		self.n_boxes = 0

		self.quads = pyglet.graphics.vertex_list(1, 'v3f', 'c3f')
		self.lines = pyglet.graphics.vertex_list(1, 'v3f', 'c3f')

		self.animating = dict()

		pyglet.clock.schedule_interval(self.animate, 1/60)


	def on_mouse_motion(self, x, y, dx, dy):
		w,h = self.get_size()

		c = min(self.x_boxes-1, x // self.box_w)
		r = min(self.y_boxes-1, y // self.box_h)

		i = c + r*self.x_boxes

		self.animating[i] = 0.6


	def animate(self, dt):
		for i in self.animating.keys():
			z = self.animating[i]

			c = i %  self.x_boxes
			r = i // self.x_boxes

			z = max(0, z-2*dt)

			self.quads.colors[12*i : 12*i+12] = [self.box_color[0]-z, self.box_color[1]-z, self.box_color[2],
			                                     self.box_color[0]-z, self.box_color[1]-z, self.box_color[2],
			                                     self.box_color[0]-z, self.box_color[1]-z, self.box_color[2],
			                                     self.box_color[0]-z, self.box_color[1]-z, self.box_color[2]]

			if z <= 0:
				del self.animating[i]
				pass
			else:
				self.animating[i] = z


	def on_resize(self, width, height):
		super(GridWindow, self).on_resize(width, height)

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
		self.lines.resize(2*(x_boxes + y_boxes + 2))

		for r in xrange(y_boxes+1):
			i = r
			self.lines.vertices[6*i : 6*i+6] = [0.0,r*self.box_h,0.0, x_boxes*self.box_w,r*self.box_h,0.0]
			self.lines.colors[6*i : 6*i+6] = [self.line_color[t%3] for t in range(6)]
		for c in xrange(x_boxes+1):
			i = c + y_boxes + 1
			self.lines.vertices[6*i : 6*i+6] = [c*self.box_w,0.0,0.0, c*self.box_w,y_boxes*self.box_h,0.0]
			self.lines.colors[6*i : 6*i+6] = [self.line_color[t%3] for t in range(6)]

		for i in xrange(n_boxes):
			c = i %  x_boxes
			r = i // x_boxes

			self.quads.vertices[12*i : 12*i+12] = [c*self.box_w,     r*self.box_h,     0,
			                                       (c+1)*self.box_w, r*self.box_h,     0,
			                                       (c+1)*self.box_w, (r+1)*self.box_h, 0,
			                                       c*self.box_w,     (r+1)*self.box_h, 0]

			self.quads.colors[12*i : 12*i+12] = [self.box_color[t%3] for t in range(12)]

			#self.quads.colors[12*i : 12*i+12] = [r*c/n_boxes, c/x_boxes/2, r/y_boxes/2,
			#                                 r*c/n_boxes, c/x_boxes/2, r/y_boxes/2,
			#                                 r*c/n_boxes, c/x_boxes/2, r/y_boxes/2,
			#                                 r*c/n_boxes, c/x_boxes/2, r/y_boxes/2] 


	def on_draw(self):
		self.clear()

		self.quads.draw(pyglet.gl.GL_QUADS)
		self.lines.draw(pyglet.gl.GL_LINES)

		fps.draw()


if __name__ == '__main__':
	window = GridWindow(resizable=True)
	pyglet.app.run()
