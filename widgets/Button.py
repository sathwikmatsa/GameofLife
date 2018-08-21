import pygame, time, sys
from pygame.locals import *
from pygame import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)

class Button:

	def __init__(self, x, y, width, height, text, fillColor, outColor, tFore, tBack, rounded):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x, y ,width, height)
		self.text = text
		self.fillColor = fillColor
		self.antiFill = outColor
		self.antiOut = fillColor
		self.outColor = outColor
		self.tFore = tFore
		self.antitF = tBack
		self.antitB = tFore
		self.tBack = tBack
		self.isRounded = rounded
		self.textRect = None
		self.state = 0

	def handle_event(self, event):
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.fillColor = self.antiFill
				self.outColor = self.antiOut
				self.tFore, self.tBack = self.antitF, self.antitB
				if event.type == MOUSEBUTTONDOWN:
					if self.state == 0:
						self.state = 1
					elif self.state == 1:
						self.state = 2
					else:
						self.state = 1
					print('pressed')
					return True
			else:
				self.fillColor = self.antiOut
				self.outColor = self.antiFill
				self.tFore, self.tBack = self.antitB, self.antitF

	def draw(self, screen):
		textFont = Button.suitableFont(self.text, None, 30, self.rect)

		textSurf = textFont.render(self.text,True, self.tFore)
		textRect = textSurf.get_rect()

		Button.DrawRect(screen, self.rect, self.fillColor,  0.4 if self.isRounded else 0)

		textRect.center = self.rect.center
		screen.blit(textSurf, textRect)

	def get_rect(self):
		return self.rect

	def set_rect(self, r):
		self.x, self.y = r.topleft
		self.rect = r

	def set_xy(self, topleft, offsetY = 0, offsetX = 0):
		if offsetY!=0 or offsetX!=0:
			topleft = list(topleft)
			topleft[0]+= offsetX
			topleft[1]+= offsetY

		self.x , self.y = topleft
		self.rect.topleft = tuple(topleft)

	def wrap_text(self):
		textFont = Button.suitableFont(self.text, None, 30, self.rect)

		textSurf = textFont.render(self.text,True, self.tFore, self.tBack)
		textRect = textSurf.get_rect()

		self.rect.height = textRect.height + 10
		self.rect.width = textRect.width + 10

	def update(self):
		return self.state

	def update_text(self, text):
		self.text = text

	def DrawRect(surface,rect,color,radius=0.4):

	    """
	    DrawRect(surface,rect,color,radius=0.4)

	    surface : destination
	    rect    : rectangle
	    color   : rgb or rgba
	    radius  : 0 <= radius <= 1
	    """

	    rect         = Rect(rect)
	    color        = Color(*color)
	    alpha        = color.a
	    color.a      = 0
	    pos          = rect.topleft
	    rect.topleft = 0,0
	    rectangle    = Surface(rect.size,SRCALPHA)

	    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
	    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
	    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

	    radius              = rectangle.blit(circle,(0,0))
	    radius.bottomright  = rect.bottomright
	    rectangle.blit(circle,radius)
	    radius.topright     = rect.topright
	    rectangle.blit(circle,radius)
	    radius.bottomleft   = rect.bottomleft
	    rectangle.blit(circle,radius)

	    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
	    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

	    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
	    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

	    return surface.blit(rectangle,pos)

	def suitableFont(text, font, maxSize, rect):
		fSize = maxSize
		FontObject = pygame.font.Font(font, fSize)
		tw, th = FontObject.size(text)
		
		while tw > rect.width or th*1.01 > rect.height:
			fSize-=1
			FontObject = pygame.font.Font(None ,fSize)
			tw, th = FontObject.size(text)

		return FontObject

def main():
    FPSCLOCK = pygame.time.Clock()
    button = Button(100, 100, 100, 20, 'Press Me', WHITE, BLACK, BLACK, WHITE, 0)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            button.handle_event(event)

        DISPLAYSURF.fill(BLACK)
        button.draw(DISPLAYSURF)

        pygame.display.flip()
        FPSCLOCK.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()
