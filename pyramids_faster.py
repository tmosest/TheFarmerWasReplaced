from hats import random_hats
from traversal import move_to
from dig_util import *
from mega_farm import wait_for_drones
from pyramids import fill_pyramid_parallel, harvest_flower
	
def pyramid_faster_parallel():
	dont_dig_set = {Grounds.Sand}
	map = dig_tracking_parallel(dont_dig_set)
	while Grounds.Sand not in map:
		map = dig_tracking_parallel(dont_dig_set)
	pos = map[Grounds.Sand][0]
	move_to(pos[0], pos[1])
	while get_ground_type() != Grounds.Limestone:
		dig()
	z = get_pos_z()
	dig_to_z_parallel(z)
	positions = dig_and_search_parallel(Grounds.Limestone)
	fill_pyramid_parallel(positions)
	harvest_flower(positions)
	dig_field_parallel()	

if __name__ == "__main__":
	clear()
	jump(Unlocks.Pyramid)
	while True:
		pyramid_faster_parallel()
