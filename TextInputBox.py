import pygame, time, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
BASICFONT = pygame.font.Font(None ,30)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
INPUT = ''

def editInput(x):
	global INPUT
	INPUT = x

def validInput(x):
	return x.isdigit()

class TextInputBox:

	def __init__(self, x , y, width, height, f, g, text=''):
		self.rect = pygame.Rect(x, y ,width, height)
		self.color = COLOR_INACTIVE
		self.text = text
		self.surface = BASICFONT.render(text, True, self.color)
		self.active = False
		self.f = f
		self.g = g

	def handle_event(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.text == "*INVALID*":
				self.text = ''
				self.surface = BASICFONT.render(self.text, True, self.color)
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False

			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
		if event.type == KEYDOWN:
			if self.active:
				if event.key == K_RETURN:
					if self.g(self.text):
						self.f(self.text)
					else:
						self.text = "*INVALID*"
						self.active = False
					self.color = COLOR_INACTIVE
				elif event.key == K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.surface = BASICFONT.render(self.text, True, self.color)

	def update(self):
		width = max(200, self.surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect, 2)
		screen.blit(self.surface, (self.rect.x+5, self.rect.y+5))

def main():
    FPSCLOCK = pygame.time.Clock()
    input_box = TextInputBox(100, 100, 140, 32, editInput, validInput)
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
    print(INPUT)