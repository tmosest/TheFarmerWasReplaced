from hats import random_hats
from mega_farm import wait_for_drones
from traversal import move_to
from dig_util import dig_to_column

def dig_column():
	random_hats()
	for _ in range(get_world_size()):
		dig()
		move(North)
		
def dig_to_mushrooms_column():
	dig_to_column(Grounds.Mushroom)
		
def harvest_mushrooms_column():
	random_hats()
	
	for _ in range(get_world_size()):
		
		mushroom = measure()

		move(East)
		
		next_mushroom = measure()
		
		move(West)
		
		if next_mushroom == mushroom:
			push(East)
			
		else:
			dig()
			
		move(North)
		
		
def dig_parallel_to_mushrooms():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(dig_to_mushrooms_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)
	

def dig_parallel_odd():
	drones = []
	for i in range(get_world_size()):
		if i % 2 == 1:
			drones.append(spawn_drone(dig_column))
		move(East)
		
	wait_for_drones(drones)

def push_mushrooms_parallel():
	drones = []
	for i in range(get_world_size()):
		if i % 2 == 0:
			drones.append(spawn_drone(harvest_mushrooms_column))
		move(East)
		
	wait_for_drones(drones)
	
def harvest_mushrooms_parallel():
	move_to(0, 0)
	while get_ground_type() == Grounds.Mushroom:
		dig_parallel_odd()
		move_to(0, 0)
		push_mushrooms_parallel()
	
if __name__ == "__main__":
	jump(Unlocks.Mushrooms)
	dig_parallel_to_mushrooms()
	harvest_mushrooms_parallel()
