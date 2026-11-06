from hats import random_hats
from traversal import move_to
from dig_util import dig_field_parallel
from mega_farm import wait_for_drones

def search_for_limestone_column():
	results = set()
	for _ in range(get_world_size()):
		if get_ground_type() == Grounds.Limestone:
			x, y = get_pos_x(), get_pos_y()
			results.add((x,y))
			
		move(North)
	
	if len(results) > 0:
		return results
	return False
			
		
def search_parallel():
	drones = []
	for i in range(get_world_size()):
		drones.append(spawn_drone(search_for_limestone_column))
		move(East)
	
	results = wait_for_drones(drones)
	
	found = False
	positions = set()
	for result in results:
		if result != False:
			found = True
			for pos in result:
				positions.add(pos)
	
	if found:
		return positions
	return found
	
def dig_and_search_parallel():
	found = False
	
	while found == False:
		found = search_parallel()
		if found == False:
			dig_field_parallel()
			
	# print(found)
	# move_to(found[0][0], found[0][1])
	
	return found
	
# The foundation layer is always present, but there will be holes in the sand.
def restore_base(positions):
	for pos in positions:
		move_to(pos[0], pos[1])
		if get_ground_type() != Grounds.Limestone:
			dig()
			place(Grounds.Limestone)
			
def get_z_position(positions):
	for pos in positions:
		move_to(pos[0], pos[1])
		return get_pos_z()
		
	return False
	
def dig_to_z_column(z):
	for _ in range(get_world_size()):
		while get_pos_z() > z:
			dig()
		move(North)
		
def dig_to_z_parallel(z):
	drones = []
	for i in range(get_world_size()):
		drones.append(spawn_drone(dig_to_z_column, z))
		move(East)
	
	results = wait_for_drones(drones)
	
def flatten_to_positions(positions):
	z = get_z_position(positions)
	dig_to_z_parallel(z)
			
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
	positions = dig_and_search_parallel()
	flatten_to_positions(positions)
	fill_pyramid_parallel(positions)
	harvest_flower(positions)
	dig_field_parallel()

if __name__ == "__main__":
	# clear()
	jump(Unlocks.Pyramid)
	pyramid_parallel()
	