import random

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