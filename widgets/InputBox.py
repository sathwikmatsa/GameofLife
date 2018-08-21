import pygame, time, sys
from pygame.locals import *
from pygame import *
from Button import Button

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)


def validInput(x):
	return x.isdigit()

class InputBox:

	def __init__(self, x, y, width, height, heading, buttonText, inputValidaterFn, maxChar, text = ''):
		self.HeaderRect = pygame.Rect(x, y, width, 2*height//7)
		self.InputRect = pygame.Rect(x, y+2*height//7, width, 3*height//7)
		self.ButtonRect = pygame.Rect(x, y+ 5*height//7, width, 2*height//7)

		self.heading = heading
		self.active = False
		self.text = text
		self.color = COLOR_INACTIVE
		self.buttonText = buttonText

		self.inputValidater = inputValidaterFn

		self.setButton = Button( self.ButtonRect.x, self.ButtonRect.y, self.ButtonRect.width, self.ButtonRect.height, self.buttonText, WHITE, BLACK, DARKSLATEGRAY, WHITE, 0)
		self.maxChar = maxChar

		self.CurrentValue = None

	def draw(self, screen):
		#heading
		HeadFont = InputBox.suitableFont(self.heading, None, 30, self.HeaderRect)
		HeadSurf = HeadFont.render(self.heading, True, WHITE, None)
		screen.blit(HeadSurf, self.HeaderRect)

		#resizing Header Rect & moving InputRect
		HTextRect = HeadSurf.get_rect()
		self.HeaderRect.height = HTextRect.height + 5

		self.InputRect.topleft = self.HeaderRect.bottomleft

		#inputtext
		InputFont = InputBox.suitableFont(self.text, None, 30, self.InputRect)
		InputSurf = InputFont.render(self.text, True, WHITE, None)
		screen.blit(InputSurf, self.InputRect)

		#resizing textbox & button
		IRect = InputSurf.get_rect()
		self.InputRect.height = IRect.height + 5
		self.setButton.wrap_text()
		self.setButton.set_xy(self.InputRect.bottomleft, 5)

		#textbox
		pygame.draw.rect(screen, self.color, self.InputRect, 2)

		#setbutton & resize ButtonRect
		self.setButton.draw(screen)
		self.ButtonRect = self.setButton.get_rect()

	def handle_event(self, event):
		if(self.setButton.handle_event(event)):
			if self.inputValidater(self.text):
				print(self.text)
				self.CurrentValue = int(self.text)
			else:
				self.reset()
				return

		if event.type == MOUSEBUTTONDOWN:
			if self.text == "*INVALID*":
				self.text = ''
			if self.InputRect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False

			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

		elif event.type == KEYDOWN:
			if self.active:
				if event.key == K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode

	def update(self):
		if len(self.text) > self.maxChar:
			self.reset()
		return self.CurrentValue

	def reset(self):
		self.text = "*INVALID*"
		self.active = False
		self.color = COLOR_INACTIVE

	def get_rect(self):
		R = pygame.Rect(0,0,0,0)
		R.topleft = self.HeaderRect.topleft
		R.width = self.InputRect.width
		R.height = self.ButtonRect.bottom - self.HeaderRect.top
		return R

	def set_rect(self, r):
		x = r.x
		y = r.y
		width = r.width
		height = r.height

		self.HeaderRect = pygame.Rect(x, y, width, 2*height//7)
		self.InputRect = pygame.Rect(x, y+2*height//7, width, 3*height//7)
		self.ButtonRect = pygame.Rect(x, y+ 5*height//7, width, 2*height//7)

	def suitableFont(text, font, maxSize, rect):
		fSize = maxSize
		FontObject = pygame.font.Font(font, fSize)
		tw, th = FontObject.size(text)
		
		while tw > rect.width or th*1.01 > rect.height:
			fSize-=1
			FontObject = pygame.font.Font(None ,fSize)
			tw, th = FontObject.size(text)

		return FontObject

	def set_value(self, val):
		self.CurrentValue = val
		self.text = str(val)

def main():
	FPSCLOCK = pygame.time.Clock()
	input_box = InputBox(100, 100, 100, 300, 'ENTER INPUT:', 'SET', validInput, 4)
	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == QUIT:
				done = True
			input_box.handle_event(event)

		input_box.update()

		DISPLAYSURF.fill((30, 30, 30))
		input_box.draw(DISPLAYSURF)

		pygame.display.flip()
		FPSCLOCK.tick(30)


if __name__ == '__main__':
	main()
	pygame.quit()