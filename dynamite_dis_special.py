# TODO run dynamite_full in here after refactor.
from traversal import move_to, move_to_center
from dig_util import dig_parallel_to_ground

clear()
jump(Unlocks.Dynamite)
print(get_pos_z())
while get_pos_z() > -600:
	dig()
while get_ground_type() != Grounds.Dynamite:
	dig()
# dig_parallel_to_ground(Grounds.Dynamite)