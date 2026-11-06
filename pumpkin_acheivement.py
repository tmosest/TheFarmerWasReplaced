clear()
change_hat(Hats.Brown_Hat)
world_size = get_world_size()
needs_till=True
 
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
 
def till_column():
	for _ in range(world_size):
		till()
		move(North)
 
def plant_first_batch():
	for _ in range(world_size):
		plant(Entities.Pumpkin)
		move(North)
		
def plant_nth_batch():
	for _ in range(world_size):
		while not can_harvest():
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
			use_item(Items.Fertilizer)
		move(North)
 
def check_done():
	return measure()==measure(South)
	
def drone_plant_loop():
	if needs_till:
		till_column()
	plant_first_batch()
	while not check_done():
		plant_nth_batch()
	
def plant_pumpkins():
	for _ in range(world_size-1):
		spawn_drone(drone_plant_loop)
		move(East)
	drone_plant_loop()
	while num_drones()>1:
		pass
	harvest()
	move(East)
 
while True:
	plant_pumpkins()
	needs_till=False