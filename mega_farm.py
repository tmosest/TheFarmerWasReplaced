from harvest import bush, carrot
from hats import random_hats
	
def wait_for_drones(drones):
	results = []
	for drone in drones:
		if drone != None:
			results.append(wait_for(drone))
	return results
	
def tree():
	if can_harvest():
		harvest()
		plant(Entities.Tree)
		# use_item(Items.Fertilizer)
		
def harvest_wood(i, j):
	if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
		tree()
	else:
		bush()

def harvest_column():
	random_hats()
	for _ in range(get_world_size()):
		harvest()
		move(North)

def harvest_column_bush():
	for _ in range(get_world_size()):
		# use_item(Items.Fertilizer)
		bush()
		move(North)
		
def harvest_column_carrot():
	for _ in range(get_world_size()):
		use_item(Items.Water)
		carrot()
		move(North)
		
def harvest_column_tree():
	for _ in range(get_world_size()):
		tree()
		move(North)
		
def harvest_column_tree_bush():
	for _ in range(get_world_size()):
		use_item(Items.Water)
		i, j = get_pos_x(), get_pos_y()
		harvest_wood(i, j)
		move(North)

def harvest_grass():
	clear()
	while True:
		if spawn_drone(harvest_column):
			move(East)
			harvest()
		
def harvest_bush():
	clear()
	while True:
		if spawn_drone(harvest_column_bush):
			move(East)
			
def harvest_tree_bush():
	clear()
	while True:
		if spawn_drone(harvest_column_tree_bush):
			move(East)
			
def harvest_carrot():
	clear()
	while True:
		if spawn_drone(harvest_column_carrot):
			move(East)
		else:
			do_a_flip()

def harvest_tree():
	clear()
	while True:
		if spawn_drone(harvest_column_tree):
			move(East)
		else:
			do_a_flip()
		
# harvest_grass()
# harvest_bush()
# harvest_carrot()
# harvest_tree()
# harvest_tree_bush()