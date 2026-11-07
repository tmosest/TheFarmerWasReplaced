from dig_util import dig_tracking_parallel
from mushrooms import harvest_mushrooms_parallel
from pyramids_faster import pyramid_faster_parallel
from ctf_treasure import treasure_map

def dig_column():
	random_hats()
	for _ in range(get_world_size()):
		if get_ground_type() != Grounds.Mushroom: # and get_ground_type() != Grounds.Clay:
			dig()
		move(North)

def dig_parallel():
	dont_dig_set = {Grounds.Sand, Grounds.Mushroom, Grounds.Basalt}
	
	while True:
		map = {}
		while Grounds.Sand not in map and get_ground_type() not in dont_dig_set:
			map = dig_tracking_parallel(dont_dig_set)
		
		if get_ground_type() == Grounds.Mushroom:
			harvest_mushrooms_parallel()
			
		if get_ground_type() == Grounds.Basalt:
			treasure_map()
			
		if Grounds.Sand in map:
			pyramid_faster_parallel()
		
if __name__ == "__main__":
	jump(Unlocks.Pyramid)
	dig_parallel()	