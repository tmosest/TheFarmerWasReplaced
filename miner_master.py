from traversal import move_to, move_to_center

def dig_north():
	# change_hat(Hats.Explosive_Drill)
	for _ in range(get_world_size()):
		dig()
		move(North)

if __name__ == "__main__":
	clear()
	# move_to()
	# for _ in range(get_world_size() - 1):
	#	spawn_drone(dig_north)
	#	move(East)
	# dig_north()
	move_to_center()
	change_hat(Hats.Explosive_Drill)
	while True:
		dig()