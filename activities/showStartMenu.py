#start menu of Game of Life

import pygame, sys, time, random
sys.path.append('../widgets')
from pygame.locals import *
from Button import Button
from ListView import ListView

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, TITLEFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font(None ,30)
	TITLEFONT = pygame.font.Font('../assets/ka1.ttf',50)
	pygame.display.set_caption('Game of Life')

	titleAnimationOnStartMenu()
	showStartMenu()
	terminate()



def titleAnimationOnStartMenu():
	titleSurf = TITLEFONT.render('Game of Life', False, WHITE, BLACK)
	titleRect = titleSurf.get_rect()
	titleRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
	while True:
		DISPLAYSURF.fill(BLACK)
		DISPLAYSURF.blit(titleSurf, titleRect)
		pygame.display.update()
		titleRect.center = (titleRect.centerx, titleRect.centery-1) # move to up
		if(titleRect.centery <= WINDOWHEIGHT//5):
			return
		FPSCLOCK.tick()

def showStartMenu():
	titleSurf = TITLEFONT.render('Game of Life', False, WHITE, BLACK)
	titleRect = titleSurf.get_rect()
	titleRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//5)
	L = ListView( 2*WINDOWWIDTH//5, WINDOWHEIGHT//3, WINDOWWIDTH//5, 3*WINDOWHEIGHT//4, 10, 10)
	RS = Button(0, 0, 100, 50, 'Random State', WHITE, BLACK, DARKSLATEGRAY, WHITE, 0)
	LS = Button(0, 0, 100, 50, 'Load State', WHITE, BLACK, DARKSLATEGRAY, WHITE, 0)
	SS = Button(0, 0, 100, 50, 'Set State', WHITE, BLACK, DARKSLATEGRAY, WHITE, 0)
	PS = Button(0, 0, 100, 50, 'Pop States', WHITE, BLACK, DARKSLATEGRAY, WHITE, 0)

	L.add_widget(RS)
	L.add_widget(LS)
	L.add_widget(SS)
	L.add_widget(PS)

	widgets = [RS, LS, SS, PS]

	while True:
		DISPLAYSURF.blit(titleSurf, titleRect)
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				return
			for widget in widgets:
				widget.handle_event(event)

		for widget in widgets:
			widget.draw(DISPLAYSURF)

		L.update(DISPLAYSURF)

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
	# try:
	#   main()
	# except Exception as e:
	#   print(str(e))
	#   terminate()
