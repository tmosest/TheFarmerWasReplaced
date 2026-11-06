# https://steamcommunity.com/app/2060160/discussions/0/824857476142774115/
# There is certainly room for improvement, but it does the job.
# This code is not sufficient to achieve 20M in 1 minute, 
# but there are now other players who have shared their excellent codes for this, 
# so I invite you to visit them if you need to!

clear()
change_hat(Hats.Brown_Hat)
world_size = get_world_size()
first_pass = True

def check_pumpkin():
	if get_pos_x() != 0:
		move(East)
	
	left_id = measure()
	move(West)
	right_id = measure()
	move(East)
	
	return left_id == right_id

def wait_for_drones(drones):
	for drone in drones:
		wait_for(drone)

def plant_column():
	global world_size
	global first_pass
	
	for j in range(world_size):
		if get_entity_type() != Entities.Pumpkin:
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
				
			if not first_pass:
				while not can_harvest():
					if get_entity_type() == Entities.Dead_Pumpkin:
						plant(Entities.Pumpkin)
					use_item(Items.Fertilizer)
		
		move(North)
	
	if not first_pass:
		for j in range(world_size):
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
			
			move(North)
	
def plant_pumpkins():
	global world_size
	global first_pass
	
	drones = []
	
	if get_pos_x() != 0:
		move(East) 
	
	for i in range(world_size - 1):
		drones.append(spawn_drone(plant_column))
		move(East)
	
	plant_column() 
	wait_for_drones(drones)

while True:
	plant_pumpkins()
	first_pass = False
	
	if check_pumpkin():
		harvest() 
		first_pass = True
		move(West)