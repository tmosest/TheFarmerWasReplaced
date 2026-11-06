# TODO update code to use rice file instead once bug is fixed
from hats import random_hats
from mega_farm import wait_for_drones
from mushrooms import harvest_mushrooms_parallel
from rice import generate_rice_parallel

def dig_column():
	random_hats()
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Mushroom: # and get_ground_type() != Grounds.Clay:
			dig()
		move(North)

def dig_parallel():
	while True:
		drones = []
		while get_ground_type() != Grounds.Mushroom: #and get_ground_type() != Grounds.Clay:
			drone = spawn_drone(dig_column)
			if drone:
				drones.append(drone)
				move(East)
		wait_for_drones(drones)
		
		if get_ground_type() == Grounds.Mushroom:
			harvest_mushrooms_parallel()
		# generate_rice_parallel()

if __name__ == "__main__":
	jump(Unlocks.Rice)
	dig_parallel()	