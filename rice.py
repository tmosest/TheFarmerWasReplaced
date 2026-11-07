# Bug keeps going straight down after it gets past the rice...
from dig_util import dig_parallel_to_ground
from mega_farm import wait_for_drones

	
def plant_rice_column():
	for _ in range(get_world_size()):
		if get_ground_type() == Grounds.Clay:
			plant(Entities.Rice)
		
		move(North)
		
def plant_rice_parallel():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(plant_rice_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)
	
def harvest_rice_column():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Rice:
			harvest()
		
		move(North)
		
def harvest_rice_parallel():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(harvest_rice_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)
	
def generate_full_rice_parallel():
	while get_ground_type() == Grounds.Clay or get_ground_type() == Grounds.Dry_Rice_Terrace or get_ground_type() == Grounds.Rice_Terrace:
		dig_parallel_to_ground(Grounds.Clay)
		plant_rice_parallel()
		harvest_rice_parallel()
		
def generate_rice_column():
	for _ in range(get_world_size()):
		if get_ground_type() == Grounds.Clay:
			plant(Entities.Rice)
		elif get_entity_type() == Entities.Rice:
			harvest()
		elif get_ground_type() == Grounds.Dry_Rice_Terrace or get_ground_type() == Grounds.Rice_Terrace or get_ground_type() == Grounds.Dirt:
			dig()
		move(North)

# Doesnt really work the way I wanted it to...
def generate_rice_parallel():
	while get_ground_type() == Grounds.Clay or get_ground_type() == Grounds.Dry_Rice_Terrace or get_ground_type() == Grounds.Rice_Terrace or get_ground_type() == Grounds.Dirt:
		drones = []
		
		i = 0
		while i < get_world_size():
			drone = spawn_drone(generate_rice_column)
			if drone:
				drones.append(drone)
				move(East)
				i = i + 1
			
		wait_for_drones(drones)
		
if __name__ == "__main__":
	clear()
	jump(Unlocks.Rice)
	dig_parallel_to_ground(Grounds.Clay)
	generate_full_rice_parallel()
	# generate_rice_parallel()
	