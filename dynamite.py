from hats import random_hats
from mega_farm import wait_for_drones
from traversal import move_to
from dig_util import dig_to_column

def dig_to_dynamite_column():
	dig_to_column(Grounds.Dynamite)
	
def dig_parallel_to_dynamite():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(dig_to_dynamite_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)

if __name__ == "__main__":
	jump(Unlocks.Dynamite)
	dig_parallel_to_dynamite()
	