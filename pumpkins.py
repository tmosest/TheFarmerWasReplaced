from traversal import move_to

def harvest_pumpkins():
	clear()
	count = 0
	while True:
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				# action_function(i, j)
				if get_entity_type() != Entities.Pumpkin:
					if get_ground_type() != Grounds.Soil:
						till()
					plant(Entities.Pumpkin)
					count = count + 1
				elif get_entity_type() == Entities.Pumpkin:
					count = count - 1
				
				if count <= 0:
					harvest()
					count = 0
				
				move(North)
			move(East)

def get_dead_count():
	count = 0
	move_to(0, 0)
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				count = count + 1
				plant(Entities.Pumpkin)
			move(North)
		move(East)
	print(count)
	return count

def make_largest_pumpkin():
	clear()
	count = 0 
	while True:
		for i in range(get_world_size()):
			for j in range(get_world_size()):
			
				if get_entity_type() != Entities.Pumpkin:
					if get_ground_type() != Grounds.Soil:
						till()
					plant(Entities.Pumpkin)
			
				move(North)
			move(East)
		
		count = get_dead_count()
		
		if count == 0:
			harvest()
			
		
		
# harvest_pumpkins()
# get_dead_count()
make_largest_pumpkin()