import random, time

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

def render(board_state):  #terminal output
	U_BLOCK = "\u2580"
	L_BLOCK = "\u2586"
	F_BLOCK = "\u2588"
	w = len(board_state)
	h = len(board_state[0])
	
	# upper border
	# for i in range(w+2):
	# 	print(L_BLOCK,end="")
	# print("")

	# content with side borders
	for i in range(w):
		#print(F_BLOCK,end="")
		for j in range(h):
			if board_state[i][j] == 1:
				print(L_BLOCK,end="")
			else:
				print(" ",end="")
		print("")
		#print(F_BLOCK)

	# lower border
	# for i in range(w+2):
	# 	print(U_BLOCK,end="")
	# print("")

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

def resizeWithPadding(board, screen_width, screen_height):
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
