#start menu of Game of Life

import pygame, sys, time, random
from pygame.locals import *

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
SIMTYPE = 0

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, TITLEFONT, SIMTYPE

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font(None ,30)
	TITLEFONT = pygame.font.Font('ka1.ttf',50)
	pygame.display.set_caption('Game of Life')

	showStartScreen()
	titleAnimationOnStartMenu()
	showStartMenu()
	print(SIMTYPE)
	terminate()


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

def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to begin.', True,  LIGHTGRAY, BLACK)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def drawButton(text, midtop, tFore, tBack, bFill, bOut, width, yPad):
	tw, th = BASICFONT.size(text)
	assert tw < width, "Button width must be greater than text width"

	textSurf = BASICFONT.render(text,True, tFore, tBack)
	textRect = textSurf.get_rect()

	button = pygame.Rect( 0, 0, width, th + 2*yPad)
	button.midtop = midtop

	pygame.draw.rect(DISPLAYSURF, bFill, button, 0) # button fill color
	pygame.draw.rect(DISPLAYSURF, bOut, button, 2) # button outline

	textRect.center = button.center
	DISPLAYSURF.blit(textSurf, textRect)
	return button

def showStartScreen():
	titleSurf = TITLEFONT.render('Game of Life', False, WHITE, BLACK)
	titleRect = titleSurf.get_rect()
	titleRect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
	board = random_state(WINDOWWIDTH//CELLWIDTH, WINDOWHEIGHT//CELLHEIGHT)
	while True:
		DISPLAYSURF.fill(BLACK)
		drawGrid(board, CELLWIDTH, CELLHEIGHT, CELLWIDTH//4, WHITE, BLACK, 0, 0)
		DISPLAYSURF.blit(titleSurf, titleRect)
		drawPressKeyMsg()

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				return
		
		pygame.display.update()
		board = next_board_state(board)
		time.sleep(0.5)
		FPSCLOCK.tick(FPS)

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
	bRS = drawButton('Random State', (WINDOWWIDTH//2, WINDOWHEIGHT//2 - 60), BLACK, BLACK, BLACK, BLACK, WINDOWWIDTH//2, 20)
	bLS = drawButton('Load State', (WINDOWWIDTH//2, WINDOWHEIGHT//2), BLACK, BLACK, BLACK, BLACK, WINDOWWIDTH//2, 20)
	bSS = drawButton('Set State', (WINDOWWIDTH//2, WINDOWHEIGHT//2 + 60), BLACK, BLACK, BLACK, BLACK, WINDOWWIDTH//2, 20)
	bPS = drawButton('Pop States', (WINDOWWIDTH//2, WINDOWHEIGHT//2 + 120), BLACK, BLACK, BLACK, BLACK, WINDOWWIDTH//2, 20)
	while True:
		DISPLAYSURF.blit(titleSurf, titleRect)
		#drawButton(text, midtop, tFore, tBack, bFill, bOut, width, yPad)
		bRS = drawButton('Random State', (WINDOWWIDTH//2, WINDOWHEIGHT//2 - 60), WHITE if not bRS.collidepoint(pygame.mouse.get_pos()) else BLACK, None, DARKSLATEGRAY if not bRS.collidepoint(pygame.mouse.get_pos()) else WHITE, GRAY, WINDOWWIDTH//2, 20)
		bLS = drawButton('Load State', (WINDOWWIDTH//2, WINDOWHEIGHT//2), WHITE if not bLS.collidepoint(pygame.mouse.get_pos()) else BLACK, None, DARKSLATEGRAY if not bLS.collidepoint(pygame.mouse.get_pos()) else WHITE, GRAY, WINDOWWIDTH//2, 20)
		bSS = drawButton('Set State', (WINDOWWIDTH//2, WINDOWHEIGHT//2 + 60), WHITE if not bSS.collidepoint(pygame.mouse.get_pos()) else BLACK, None, DARKSLATEGRAY if not bSS.collidepoint(pygame.mouse.get_pos()) else WHITE, GRAY, WINDOWWIDTH//2, 20)
		bPS = drawButton('Pop States', (WINDOWWIDTH//2, WINDOWHEIGHT//2 + 120), WHITE if not bPS.collidepoint(pygame.mouse.get_pos()) else BLACK, None, DARKSLATEGRAY if not bPS.collidepoint(pygame.mouse.get_pos()) else WHITE, GRAY, WINDOWWIDTH//2, 20)
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == MOUSEBUTTONUP:
				if optionSelected([bRS, bLS, bSS, bPS]):
					return
			elif event.type == KEYDOWN:
				return
		pygame.display.update()
		FPSCLOCK.tick(FPS)

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

##### Manipulating Data structure #####

def dead_state(width, height):
	state = []
	for i in range(width):
		state.append([0]*height)
	return state

def random_state(width, height, threshold = 0.5):
	ALIVE = 1
	DEAD = 0

	state = dead_state(width, height)

	for i in range(width):
		for j in range(height):
			if random.random() < threshold:
				state[i][j] = ALIVE

	return state

def next_board_state(board_state):

	width = len(board_state)
	height = len(board_state[0])
	new_state = dead_state(width, height)

	def isCorner(x, y):
		if x==y==0 or (x==0 and y==height-1) or (x==width-1 and y==0) or (x==width-1 and y==height-1):
			return True
		else:
			return False
	def isEdge(x, y):
		if y==0 or y==height-1 or x==0 or x==width-1:
			return True # returns True for corner, to avoid this we call it after isCorner()
		else:
			return False

	def get_alive_neighbours_count(x, y):
		count = 0
		if(isCorner(x,y)):
			count+=board_state[x][y-1 if y==height-1 else y+1]  #x
			count+=board_state[ x-1 if x==width-1 else x+1][y] #y
			count+=board_state[ x-1 if x==width-1 else x+1][ y-1 if y==height-1 else y+1] #diag
		elif(isEdge(x,y)):
			count+= board_state[x-1][y-1] if x!=0 and y!=0 else 0
			count+= board_state[x-1][y] if x!=0 else 0
			count+= board_state[x-1][y+1] if x!=0 and y!=height-1 else 0
			count+= board_state[x][y-1] if y!=0 else 0
			count+= board_state[x][y+1] if y!=height-1 else 0
			count+= board_state[x+1][y-1] if x!=width-1 and y!=0 else 0
			count+= board_state[x+1][y] if x!=width-1 else 0
			count+= board_state[x+1][y+1] if x!=width-1 and y!=height-1 else 0
		else:
			count+=board_state[x-1][y-1]
			count+=board_state[x-1][y]
			count+=board_state[x-1][y+1]
			count+=board_state[x][y-1]
			count+=board_state[x][y+1]
			count+=board_state[x+1][y-1]
			count+=board_state[x+1][y]
			count+=board_state[x+1][y+1]

		return count

	def rules_of_life(x,y):
		n = get_alive_neighbours_count(x,y)
		if(board_state[x][y]):
			if(n==0 or n==1): 
				#Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
				return 0
			elif(n==2 or n==3): 
				#Any live cell with 2 or 3 live neighbors stays alive, because their neighborhood is just right
				return 1
			else:
				#Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
				return 0
		else:
			if(n==3):
				#Any dead cell with exactly 3 live neighbors becomes alive, by reproduction
				return 1
			else:
				return 0

	for i in range(width):
		for j in range(height):
			new_state[i][j] = rules_of_life(i,j)

	return new_state

def load_board_state(filename):
	with open(filename,"r") as f:
		lines = f.readlines()
		lines = [line.strip() for line in lines]
		width = len(lines)
		height = len(lines[0])
		board = dead_state(width, height)
		for i in range(width):
			for j in range(height):
				board[i][j] = int(lines[i][j])

		f.close()
		return board

def pad(board, screen_width, screen_height):
	board_width = len(board)
	board_height = len(board[0])

	if board_width>screen_width or board_height>screen_height:
		return []
	elif board_width == screen_width and board_height == screen_height:
		return board

	# horizontal centering
	l_pad = (screen_width - board_width)//2
	r_pad = l_pad + (screen_width % board_width)
	for i in range(board_width):
		board[i] = [0]*l_pad + board[i] + [0]*r_pad

	# update board width
	board_width = len(board[0])

	# vertical centering
	t_pad = (screen_height - board_height)//2
	b_pad = t_pad + (screen_height % board_height)

	for i in range(t_pad):
		board.insert(0,[0]*board_width)
	for i in range(b_pad):
		board.append([0]*board_width)

	return board

if __name__ == '__main__':
	main()
	# try:
	#   main()
	# except Exception as e:
	#   print(str(e))
	#   terminate()
