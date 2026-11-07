from hats import random_hats
from traversal import move_to
from dig_util import *
from mega_farm import wait_for_drones

# This doesn't work...
if __name__ == "__main__":
	jump(Unlocks.Special_Soils)
	dig_and_search_parallel(Grounds.Perlite)
	dig_parallel_to_ground(Grounds.Perlite)