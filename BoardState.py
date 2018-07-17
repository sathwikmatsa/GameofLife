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

