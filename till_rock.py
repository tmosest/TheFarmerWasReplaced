from mega_farm import wait_for_drones

def dig_till_rock_column():
	for _ in range(get_world_size()):
		if get_ground_type() == Grounds.Rock:
			till()
		dig()
		move(North)

def dig_till_rock_parallel():
	drones = []
	
	i = 0
	while i < get_world_size():
		drone = spawn_drone(dig_till_rock_column)
		if drone:
			drones.append(drone)
			move(East)
			i = i + 1
		
	wait_for_drones(drones)

if __name__ == "__main__":
	jump(Unlocks.Iron)
	while True:
		dig_till_rock_parallel()