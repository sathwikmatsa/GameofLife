#start screen of Game of Life

import pygame, sys, time, random
sys.path.append('../widgets')
from Grid import Grid
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 19

# assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
# assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
LIGHTGRAY = ( 211, 211, 211)

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font(None ,30)
	pygame.display.set_caption('Game of Life')

	showStartScreen()
	terminate()


def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to begin.', True,  LIGHTGRAY, BLACK)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def showStartScreen():
	TITLEFONT = pygame.font.Font('../assets/ka1.ttf',50)
	titleSurf = TITLEFONT.render('Game of Life', False, WHITE, BLACK)
	titleRect = titleSurf.get_rect()
	titleRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
	grid = Grid(0, 0, WINDOWWIDTH, WINDOWHEIGHT, 30, BLACK, BLACK, WHITE)
	grid.set_random_state();
	while True:
		DISPLAYSURF.fill(BLACK)
		grid.draw(DISPLAYSURF)
		DISPLAYSURF.blit(titleSurf, titleRect)
		drawPressKeyMsg()

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				return
		
		pygame.display.update()
		time.sleep(0.5)
		FPSCLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
	terminate()
	# try:
	# 	main()
	# except Exception as e:
	# 	print(str(e))
	# 	terminate()
