from hats import random_hats
from traversal import move_to
from dig_util import *
from mega_farm import wait_for_drones
			
def get_min_max(positions):
	min_x = 1000
	max_x = 0
	min_y = 1000
	max_y = 0
	
	for pos in positions:
		min_x = min(pos[0], min_x)
		min_y = min(pos[1], min_y)
		max_x = max(pos[0], max_x)
		max_y = max(pos[1], max_y)
	
	return [(min_x, min_y), (max_x, max_y)]
	
def flatten_to_positions(positions):
	z = get_z_position(positions)
	dig_to_z_parallel(z)
	
def fill_layer(positions, min_max, i):
	for pos in positions:
		
		if i != -1 and i != pos[0]:
			continue
		
		if min_max[0][0] > pos[0]:
			continue
			
		if min_max[0][1] > pos[1]:
			continue
			
		if min_max[1][0] < pos[0]:
			continue
			
		if min_max[1][1] < pos[1]:
			continue
			
		move_to(pos[0], pos[1])
		# For normal
		# place(Grounds.Sand)
		# For the acheivement.
		place(Grounds.Block_Blue)

def fill_layer_parallel(positions, min_max):
	drones = []
	for i in range(get_world_size()):
		drones.append(spawn_drone(fill_layer, positions, min_max, i))
		move(East)
	
	results = wait_for_drones(drones)
	
def fill_pyramid_parallel(positions):
	min_max = get_min_max(positions)
	
	while min_max[0][0] <= min_max[1][0]:
		
		fill_layer_parallel(positions, min_max)
		
		min_max[0] = (min_max[0][0] + 1, min_max[0][1] + 1)
		min_max[1] = (min_max[1][0] - 1, min_max[1][1] - 1)

# Note can only harvest one flower at a time.
# This could be faster but I am lazy.
def harvest_flower(positions):
	for pos in positions:
		move_to(pos[0], pos[1])
		if get_entity_type() == Entities.Sunflower:
			harvest()
			return
			
def pyramid_parallel():
	positions = dig_and_search_parallel(Grounds.Limestone)
	flatten_to_positions(positions)
	fill_pyramid_parallel(positions)
	harvest_flower(positions)
	dig_field_parallel()

if __name__ == "__main__":
	clear()
	jump(Unlocks.Pyramid)
	pyramid_parallel()
	