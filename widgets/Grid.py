import pygame, time, sys, random
from pygame.locals import *
from pygame import *
from Button import Button

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
BASICFONT = pygame.font.Font(None ,30)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
GREEN = (0, 255, 0)
LIGHTGRAY = ( 211, 211, 211)
GRAY = (128, 128, 128)
DARKSLATEGRAY = (47, 79, 79)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
INPUT = ''

class Grid:

	def __init__(self, x , y, width, height, block_size, block_color, margin_color, selected_color):
		self.rect = pygame.Rect(x, y ,width, height)
		self.board = None
		self.x = x
		self.y = y
		self.block_color = block_color
		self.margin_color = margin_color
		self.block_size = block_size
		self.sel_color = selected_color
		self.board_state = None
		self.pause = False
		self.random = False

	def handle_event(self, event):
		if event.type == MOUSEBUTTONDOWN and self.board != None:
			c_x, c_y = event.pos
			if self.board.collidepoint(event.pos):
				Col = (c_x-self.board.x)//(self.block_size + self.margin)
				Row = (c_y-self.board.y)//(self.block_size + self.margin)
				self.board_state[Row][Col] = 1 if self.board_state[Row][Col] == 0 else 0


	def update(self, pause, scale, board = None):
		self.pause = pause
		if board != None:
			self.board_state = board

		if self.block_size != scale:
			self.block_size = scale
			self.board_state = Grid.filter_board(self.board_state)

	def set_random_state(self):
		self.random = True

	def draw(self, screen):
		pygame.draw.rect(screen, (0,0,0), self.rect, 0)
		est_margin = int(self.block_size/5)
		#self.margin = est_margin if est_margin > 0 else 1
		self.margin = est_margin
		self.h_cells = int(self.rect.width/self.block_size)
		self.v_cells = int(self.rect.height/self.block_size)

		# adjusting no. of horizontal cells to fit screen width
		while (self.h_cells*self.block_size + (self.h_cells+1)*self.margin > self.rect.width):
			self.h_cells-=1

		# adjusting no. of vertical cells to fit screen height
		while (self.v_cells*self.block_size + (self.v_cells+1)*self.margin > self.rect.height):
			self.v_cells-=1

		# pad matrix size to screen
		self.board_state = Grid.pad(self.board_state, self.h_cells, self.v_cells, self.random)
		self.random == False

		if self.board_state == None:
			self.board_state = Grid.dead_state(self.v_cells, self.h_cells)

		self.wasted_x = self.rect.width - (self.h_cells*self.block_size + (self.h_cells+1)*self.margin)
		self.wasted_y = self.rect.height - (self.v_cells*self.block_size + (self.v_cells+1)*self.margin)

		start_x = self.x + int(self.wasted_x/2)
		start_y = self.y + int(self.wasted_y/2)

		# paint background with margin color
		self.board = pygame.draw.rect(screen, self.margin_color, [start_x, start_y, self.h_cells*(self.block_size + self.margin) + self.margin, self.v_cells*(self.block_size + self.margin) + self.margin], 0)

		# draw boxes
		for y in range(self.v_cells):
			y_coord = start_y + y*(self.block_size + self.margin) + self.margin
			x_coord = start_x + self.margin
			for x in range(self.h_cells):
				if(self.board_state == None or self.board_state[y][x]==0):
					pygame.draw.rect(screen, self.block_color, [x_coord, y_coord, self.block_size, self.block_size],0)
				else:
					pygame.draw.rect(screen, self.sel_color, [x_coord, y_coord, self.block_size, self.block_size],0)

				x_coord+=self.block_size + self.margin

		self.board_state = self.board_state if self.board_state == None or self.pause else Grid.next_board_state(self.board_state)

	def reset(self):
		pass

	@staticmethod
	def dead_state(nRows, nCols):
		state = []
		for i in range(nRows):
			state.append([0]*nCols)
		return state

	def random_state(nRows, nCols, threshold = 0.5):
		ALIVE = 1
		DEAD = 0

		state = Grid.dead_state(nRows, nCols)

		for i in range(nRows):
			for j in range(nCols):
				if random.random() < threshold:
					state[i][j] = ALIVE

		return state

	def next_board_state(board_state):

		nRows = len(board_state)
		nCols = len(board_state[0])
		new_state = Grid.dead_state(nRows, nCols)

		def isCorner(x, y):
			if x==y==0 or (x==0 and y==nCols-1) or (x==nRows-1 and y==0) or (x==nRows-1 and y==nCols-1):
				return True
			else:
				return False
		def isEdge(x, y):
			if y==0 or y==nCols-1 or x==0 or x==nRows-1:
				return True # returns True for corner, to avoid this we call it after isCorner()
			else:
				return False

		def get_alive_neighbours_count(x, y):
			count = 0
			if(isCorner(x,y)):
				count+=board_state[x][y-1 if y==nCols-1 else y+1]  #x
				count+=board_state[ x-1 if x==nRows-1 else x+1][y] #y
				count+=board_state[ x-1 if x==nRows-1 else x+1][ y-1 if y==nCols-1 else y+1] #diag
			elif(isEdge(x,y)):
				count+= board_state[x-1][y-1] if x!=0 and y!=0 else 0
				count+= board_state[x-1][y] if x!=0 else 0
				count+= board_state[x-1][y+1] if x!=0 and y!=nCols-1 else 0
				count+= board_state[x][y-1] if y!=0 else 0
				count+= board_state[x][y+1] if y!=nCols-1 else 0
				count+= board_state[x+1][y-1] if x!=nRows-1 and y!=0 else 0
				count+= board_state[x+1][y] if x!=nRows-1 else 0
				count+= board_state[x+1][y+1] if x!=nRows-1 and y!=nCols-1 else 0
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

		for i in range(nRows):
			for j in range(nCols):
				new_state[i][j] = rules_of_life(i,j)

		return new_state

	def load_board_state(filename):
		with open(filename,"r") as f:
			lines = f.readlines()
			lines = [line.strip() for line in lines]
			nRows = len(lines)
			nCols = len(lines[0])
			board = dead_state(nRows, nCols)
			for i in range(nRows):
				for j in range(nCols):
					board[i][j] = int(lines[i][j])

			f.close()
			return board

	def pad(board, screen_width, screen_height, isRandom):
		rRows = screen_height
		rCols = screen_width
		if (board == None and not isRandom) or board == []:
			return Grid.dead_state(rRows, rCols)
		elif board == None and isRandom:
			return Grid.random_state(rRows, rCols)
		nRows = len(board)
		nCols = len(board[0])
		
		if nRows > rRows or nCols > rCols:
			board = Grid.filter_board(board)
			board = board[:rRows]
			board = [x[:rCols] for x in board]
			return board

		elif nRows == rRows and nCols == rCols:
			return board

		# horizontal centering
		l_pad = (rCols - nCols)//2
		r_pad = l_pad + (rCols - nCols) % 2

		for i in range(nRows):
			board[i] = [0]*l_pad + board[i] + [0]*r_pad

		# update col num
		nCols = len(board[0])

		# vertical centering
		t_pad = (rRows - nRows)//2
		b_pad = t_pad + (rRows - nRows) % 2

		for i in range(t_pad):
			board.insert(0,[0]*nCols)
		for i in range(b_pad):
			board.append([0]*nCols)

		return board

	def filter_board(board):
		nRows = len(board)
		nCols = len(board[0])
		flag = True

		rightmost_x = leftmost_x = bottommost_y = topmost_y = 0

		for i in range(nRows):
			if not flag:
				break
			for j in range(nCols):
				if board[i][j]==1:
					topmost_y = i
					flag = False
					break
		flag = True
		for i in range(nRows)[::-1]:
			if not flag:
				break
			for j in range(nCols):
				if board[i][j]==1:
					bottommost_y = i
					flag = False
					break

		flag = True
		for j in range(nCols):
			if not flag:
				break
			for i in range(nRows):
				if board[i][j]==1:
					leftmost_x = j
					flag = False
					break

		flag = True
		for j in range(nCols)[::-1]:
			if not flag:
				break
			for i in range(nRows):
				if board[i][j]==1:
					rightmost_x = j
					flag = False
					break

		new_board = Grid.dead_state(bottommost_y - topmost_y + 1, rightmost_x - leftmost_x + 1)
		for i in range(len(new_board)):
			for j in range(len(new_board[0])):
				new_board[i][j] = board[i+topmost_y][j+leftmost_x]
		
		return new_board


def main():
	FPSCLOCK = pygame.time.Clock()
	grid = Grid(0, 0, 640, 480, 20, WHITE, BLACK, GREEN)
	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == QUIT:
				done = True
			grid.handle_event(event)

		#input_box.update()

		DISPLAYSURF.fill(GRAY)
		grid.draw(DISPLAYSURF)

		pygame.display.flip()
		FPSCLOCK.tick(30)


if __name__ == '__main__':
	main()
	pygame.quit()
	print(INPUT)
