def traverse(action_function):
	while True:
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				action_function(i, j)
				move(North)
			move(East)
			
def move_to(i, j):
	x = get_pos_x()
	y = get_pos_y()
	
	while i != x or y != j:
		if i > x:
			move(East)
		elif i < x:
			move(West) 
		
		if y < j:
			move(North)
		elif y > j:
			move(South)
			
		x = get_pos_x()
		y = get_pos_y()
	
# move_to(1,1)