# Big Bamboo Farmer takes an hour.
# Bamboo Master works with this too.
# Just need to cycle restarts until it is a layer of just Perlite near by.
from hats import random_hats
from traversal import move_to
from dig_util import *
from mega_farm import wait_for_drones

def dig_to_special():
	dont_dig_set = {Grounds.Perlite, Grounds.Loam, Grounds.Clay}
	found_dont_dig = False
	while found_dont_dig == False:
			map = dig_tracking_parallel(dont_dig_set)
			for ground in dont_dig_set:
				if ground in map:
					found_dont_dig = True
	
	# This only works for clay as perlite and loam have holes...
	# for ground in dont_dig_set:
		# if ground in map:
			# dig_parallel_to_ground(ground)
					
	for _ in range(2):
		dig_tracking_parallel(dont_dig_set)
		
heights = {}

def bamboo_cell(x, y):
	global heights
			
	if get_entity_type() != Entities.Bamboo:
		if (x % 2 == 0 and y % 2 ==0) or (x % 2 == 1 and y % 2 == 1):
			if get_ground_type() == Grounds.Perlite:
				plant(Entities.Bamboo)
		
	if get_entity_type() == Entities.Bamboo:
		h = measure()
			
		previous_height = 0
		if (x,y) in heights:
			previous_height = heights[(x,y)]
			
		# if the plant hasn't grown then we mark it for harvest
		if h == previous_height:
			h = 1
				
		heights[(x,y)] = h
		
	up_y = (y + 1) % get_world_size()
		
	right_x = x
	if up_y == 0:
		right_x = (x + 1) % get_world_size()
		
	if (right_x, up_y) in heights:
		next_height = heights[(right_x, up_y)]
		hover(next_height)
	
def bamboo_grid():
	clear()
	traverse(bamboo_cell)
	
def bamboo_column():
	while True:
		# use_item(Items.Water)
		i, j = get_pos_x(), get_pos_y()
		bamboo_cell(i, j)
		move(North)
		
def bamboo_parallel():
	# clear()
	# hover(15)
	for _ in range(get_world_size() - 1):
		if spawn_drone(bamboo_column):
			move(East)
	bamboo_column()

if __name__ == "__main__":
	jump(Unlocks.Special_Soils)
	dig_to_special()
	bamboo_parallel()