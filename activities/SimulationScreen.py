#start menu of Game of Life

import pygame, sys, time, random
from pygame.locals import *
from pygame import gfxdraw
from GOL import *
from ListView import ListView
from Button import Button
from InputBox import InputBox
from Grid import Grid

FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
GREEN = (0, 255, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)
SIMTYPE = 0

PAUSE = False
SCALE = None

def validInput(x):
	return x.isdigit()

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, TITLEFONT, SIMTYPE, WINDOWWIDTH, WINDOWHEIGHT
	global PAUSE, SCALE

	pygame.init()
	infoObject = pygame.display.Info()
	WINDOWWIDTH, WINDOWHEIGHT = infoObject.current_w, infoObject.current_h
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font(None ,30)
	TITLEFONT = pygame.font.Font('ka1.ttf',50)
	pygame.display.set_caption('Game of Life')

	initSimulator()
	terminate()

def initSimulator():
	pygame.draw.rect(DISPLAYSURF, DARKSLATEGRAY, (0, 0, WINDOWWIDTH//8, WINDOWHEIGHT), 0)
	pygame.draw.line(DISPLAYSURF, GRAY, (WINDOWWIDTH//8, 0), (WINDOWWIDTH//8, WINDOWHEIGHT), 2)

	L = ListView( 0, 0, WINDOWWIDTH//8, WINDOWHEIGHT, 10, 30)
	startButton = Button(0, 0, 100, 50, 'Start', WHITE, BLACK, DARKSLATEGRAY, WHITE, 1)
	input_box = InputBox(0, 0, 100, 50, 'scale:', 'set', validInput, 4)
	taSetter = Button(0, 0, 100, 50, 'TA: OFF', WHITE, BLACK, DARKSLATEGRAY, WHITE, 1)
	
	L.add_widget(startButton)
	L.add_widget(input_box)
	L.add_widget(taSetter)

	grid = Grid(WINDOWWIDTH//8, 0, 7*WINDOWWIDTH//8, WINDOWHEIGHT, 20, WHITE, BLACK, GREEN)
	input_box.set_value(20)

	widgets = [startButton, input_box, taSetter]
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			for widget in widgets:
				widget.handle_event(event)
			grid.handle_event(event)

		PAUSE = True if startButton.update()==0 or startButton.update()==2 else False
		if PAUSE:
			if startButton.update() != 0:
				startButton.update_text('Resume')
		else:
			startButton.update_text('Pause')
		SCALE = input_box.update()
		taSetter.update()
		grid.update(PAUSE, SCALE)


		pygame.draw.rect(DISPLAYSURF, DARKSLATEGRAY, (0, 0, WINDOWWIDTH//8, WINDOWHEIGHT), 0)
		pygame.draw.line(DISPLAYSURF, GRAY, (WINDOWWIDTH//8, 0), (WINDOWWIDTH//8, WINDOWHEIGHT), 2)

		for widget in widgets:
			widget.draw(DISPLAYSURF)

		L.update(DISPLAYSURF)
		grid.draw(DISPLAYSURF)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def drawGrid(board, cellWidth, cellHeight, padding, onColor, offColor, offsetX, offsetY):
	nRows = len(board)
	nCols = len(board[0])
	y = offsetY
	for row in range(nRows):
		x = offsetX
		for column in range(nCols):
			if board[row][column]!=1:
				pygame.draw.rect(DISPLAYSURF, offColor, [x+padding, y+padding, cellWidth, cellHeight],0) 
			else:
				pygame.draw.rect(DISPLAYSURF, onColor, [x+padding, y+padding, cellWidth, cellHeight],0)
			x+=(cellWidth+padding)
		y+=(cellHeight+padding)

def optionSelected(buttonRectList):
	global SIMTYPE

	for i in range(len(buttonRectList)):
		if buttonRectList[i].collidepoint(pygame.mouse.get_pos()):
			SIMTYPE = i
			return True
	return False

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
