"""

MIT/X11 License

Copyright (c) 2009 Nicolas Crovatti.

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.


Additionnal Copyrights:

Mounts & Clouds Brushes 	: http://javierzhx.deviantart.com/
Trees Brushes 						: http://deathoflight.deviantart.com/
Grass Brushes 						: http://archeleron.deviantart.com/
"""
import pygame
from gameobjects.vector2 import Vector2


RESOLUTION = (500, 400)

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)

class AnimatedSprite(pygame.sprite.Sprite):
		def __init__(self, images, fps = 10):
			pygame.sprite.Sprite.__init__(self)
			
			# Animation 
			self._start 			= pygame.time.get_ticks()
			self._delay 			= 1000 / fps
			self._last_update = 0
			self._frame 			= 0
			self._images 			= images
			
			self.image 				= self._images[self._frame]
			
			# Movement
			self.location 		= (0,0)
			self.destination 	= (0,0)
			self.heading			= None
			self.speed				= 0.
			
			
			
		def process(self, t):
			if self.speed > 0. and self.location != self.destination:
					destination = self.destination - self.location
					distance = destination.get_length()
					self.heading = destination.get_normalized()
					most_accurate_distance = min(distance, t * self.speed)
					self.location += most_accurate_distance * self.heading
					
		def update(self, t):
			# Note that this doesn't work if it's been more that self._delay
			# time between calls to update(); we only update the image once
			# then, but it really should be updated twice.
			if t - self._last_update > self._delay:
				self._frame += 1
				if self._frame >= len(self._images):
					self._frame = 0
					
				self.image = self._images[self._frame]
				self._last_update = t
            
		def render(self, screen):
			screen.blit(self.image, self.location)


class Parallax(AnimatedSprite):
		def __init__(self, images, fps = 30):
				AnimatedSprite.__init__(self, images, fps)
		
		
		def render(self, screen):
			# Overridding the default render method
			w,h = self.image.get_size()
			x,y = self.location
			W,H = RESOLUTION
			
			# Reseting original image location 
			if abs(x) == w:
					self.location = Vector2(0, y)
					x = 0
					
			# Blitting the image loop 
			if x - w < W:
				location = Vector2(x+w, y)
				screen.blit(self.image, location)
			
			screen.blit(self.image, self.location)
