# This didn't work...
# I moved it all the way down to another stratum...
# It worked the 2nd time which was much further away
# Dynamite can ruin this...
# Got lucky wih the one below matching and did the rest manually.
from traversal import move_to
from dig_util import *

def alternating_dig():
	i = 0
	while get_ground_type() != Grounds.Mushroom:
		if i % 2 == 0:
			move_to(1, 0)
			push(East)
			dig()
		else:
			move_to(2, 0)
			push(West)
			dig()
		
		i += 1

def mushrooms_long_distance_friends():
	jump(Unlocks.Mushrooms)
	dig_parallel_to_ground(Grounds.Mushroom)
		
	move_to(1, 0)
	while get_ground_type() == Grounds.Mushroom:
		dig()
	
	move_to(2, 0)
	while get_ground_type() == Grounds.Mushroom:
		dig()
		
	move_to(0, 0)
	push(East)
	
	move_to(2, 0)
	alternating_dig()

if __name__ == "__main__":
	# mushrooms_long_distance_friends()
	# dig()
	# move_to(2, 0)
	# alternating_dig()
	# z = get_pos_z()
	# dig_to_z_parallel(z)
	# move(North)
	# dig()
	# move(North)
	# push(South)
	# move(South)
	# move(North)
	# push(North)
	# move_to(1, 0)
	# push(West)
	# move_to(0, 0)
	# push(East)
	move_to(2, 0)
	push(West)