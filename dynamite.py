from hats import random_hats
from mega_farm import wait_for_drones
from traversal import move_to, move_to_center
from dig_util import dig_parallel_to_ground

def get_circle_positions():
	x, y = get_pos_x(), get_pos_y()
	
	positions = []
	
	if x - 1 > -1:
		next_position = (x - 1, y)
		positions.append(next_position)
	
	if x + 1 < get_world_size():
		next_position = (x + 1, y)
		positions.append(next_position)
		
	if y - 1 > -1:
		next_position = (x, y - 1)
		positions.append(next_position)
	
	if y + 1 < get_world_size():
		next_position = (x, y + 1)
		positions.append(next_position)
		
	if x - 1 > -1 and y - 1 > -1:
		next_position = (x - 1, y - 1)
		positions.append(next_position)
	
	if x - 1 > -1 and y + 1 < get_world_size():
		next_position = (x - 1, y + 1)
		positions.append(next_position)
		
	if x + 1 < get_world_size() and y - 1 > -1:
		next_position = (x + 1, y - 1)
		positions.append(next_position)
	
	if x + 1 < get_world_size() and y + 1 < get_world_size():
		next_position = (x + 1, y + 1)
		positions.append(next_position)
			
	move_to(x, y)
	
	return positions
	
def dig_circle():
	positions = get_circle_positions()
	
	for position in positions:	
		move_to(position[0], position[1])
		while get_ground_type() != Grounds.Soot:
			dig()

def get_zero_positions_in_circle():
	positions = get_circle_positions()
	
	results = set()
	
	for position in positions:	
		move_to(position[0], position[1])
		if get_ground_type() == Grounds.Soot and measure() == 0:
			results.add(position)

	return results
			
def mine_zeros(start):
	stack = []
	stack.append(start)
	
	visited = set()
	
	while len(stack) > 0:
		pos = stack.pop(0)
		
		if pos not in visited:
			move_to(pos[0], pos[1])
			dig_circle()
			for position in get_zero_positions_in_circle():
				stack.append(position)
		
		visited.add(pos)

if __name__ == "__main__":
	# Bug with set world size...
	# set_world_size(16)
	jump(Unlocks.Dynamite)
	dig_parallel_to_ground(Grounds.Dynamite)
	move_to_center()
	dig()
	# Has a top right bias...
	mine_zeros((get_pos_x(), get_pos_y()))
	# mine_zeros((18, 15))