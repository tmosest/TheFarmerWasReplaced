from traversal import traverse, move_to

def plant_cactus():
	if get_ground_type() != Grounds.Soil:
			till()
	plant(Entities.Cactus)
		
def plant_all_cactus():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			plant_cactus()
			move(North)
		move(East)
	
def sort_line(start_x, start_y, direction):
	n = get_world_size()
	move_to(start_x, start_y)
	for i in range(n):
		move_to(start_x, start_y)
		swap_count = 0
		for j in range(n - 1 - i):
			if measure() > measure(direction):
				swap_count += 1
				swap(direction) 
			move(direction)
			
		if swap_count == 0:
			break
   
	
def harvest_sorted_cactus():
	n = get_world_size()
	clear()
	while True:
		clear()
		plant_all_cactus()
		
		for i in range(n):
			sort_line(i, 0, North)
		
		for i in range(n):
			sort_line(0, i, East)
			
		harvest()

#set_world_size(4)		
harvest_sorted_cactus()		