from mega_farm import wait_for_drones

def place_column():
	for _ in range(get_world_size()):
		place(Grounds.Block_Blue)
		move(North)
		
def place_blocks_parallel():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(place_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)

if __name__ == "__main__":
	clear()
	while True:
		place_blocks_parallel()