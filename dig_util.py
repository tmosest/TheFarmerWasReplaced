from hats import random_hats
from mega_farm import wait_for_drones
from traversal import move_to

def dig_to_column(ground_type):
	random_hats()
	for _ in range(get_world_size()):
		
		while get_ground_type() != ground_type:
			dig()
		
		move(North)
		
def dig_feild_column():
	for _ in range(get_world_size()):
		dig()
		move(North)

def dig_field_parallel():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(dig_feild_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)
	
def search_column(ent):
	results = set()
	for _ in range(get_world_size()):
		if get_ground_type() == ent:
			x, y = get_pos_x(), get_pos_y()
			results.add((x,y))
			
		move(North)
	
	if len(results) > 0:
		return results
	return False
	
def search_parallel(ent):
	drones = []
	for i in range(get_world_size()):
		drones.append(spawn_drone(search_column, ent))
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
	
def dig_and_search_parallel(ent):
	found = False
	
	while found == False:
		found = search_parallel(ent)
		if found == False:
			dig_field_parallel()
			
	# print(found)
	# move_to(found[0][0], found[0][1])
	
	return found
	
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