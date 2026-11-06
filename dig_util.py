from hats import random_hats
from mega_farm import wait_for_drones

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