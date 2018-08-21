import pygame, time, sys
from pygame.locals import *
from pygame import gfxdraw
from Button import Button
from InputBox import InputBox

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
BASICFONT = pygame.font.Font(None ,30)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)

def validInput(x):
	return x.isdigit()

class ListView:

	def __init__(self, x, y, width, height, borderPad, yPad):
		self.rect = pygame.Rect(x, y, width, height)
		self.upperlimit = self.rect.midtop
		self.xPad = borderPad
		self.yPad = yPad
		self.widgets = []

	def add_widget(self, widget):
		r = widget.get_rect()
		aWidth = self.rect.width - 2*self.xPad
		r.size = (aWidth, int((aWidth*r.height)/r.width))
		self.upperlimit = self.widgets[-1].get_rect().midbottom if len(self.widgets)!=0 else self.rect.midtop
		r.midtop = (self.upperlimit[0], self.upperlimit[1]+ self.yPad)
		assert r.bottom < self.rect.bottom, "no space left to accomodate the widget"
		widget.set_rect(r)
		self.widgets.append(widget)

	def update(self,screen):
		widgets = self.widgets
		self.widgets = []
		for widget in widgets:
			self.add_widget(widget)

def main():
	FPSCLOCK = pygame.time.Clock()
	button1 = Button(100, 100, 100, 20, 'PRESS ME1', WHITE, BLACK, BLACK, WHITE, 1)
	button2 = Button(100, 100, 100, 20, 'Press Me2', WHITE, BLACK, BLACK, WHITE, 1)
	button3 = Button(100, 100, 100, 20, 'Press Me3', WHITE, BLACK, BLACK, WHITE, 1)
	input_box = InputBox(100, 100, 100, 100, 'enter input:', 'set', validInput, 4)
	L = ListView( 0, 0, 100, 500, 10, 10)
	L.add_widget(button1)
	L.add_widget(button2)
	L.add_widget(button3)
	L.add_widget(input_box)
	widgets = [button1, button2, button3, input_box]
	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == QUIT:
				done = True
			for widget in widgets:
				widget.handle_event(event)
		
		input_box.update()
		
		#DISPLAYSURF.fill(BLACK)
		for widget in widgets:
			widget.draw(DISPLAYSURF)

		pygame.display.flip()
		FPSCLOCK.tick(30)


if __name__ == '__main__':
	main()
	pygame.quit()
