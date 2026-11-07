from traversal import traverse

def bamboo_sample_one():
	clear()
	till()
	plant(Entities.Bamboo)
	move(East) # move away so the bamboo can grow

def bamboo_sample_two():
	clear()
	till()
	plant(Entities.Bamboo)
	hover(measure()) # hover such that drone will be next to fruit
	
	move(East) # move away and wait for it to grow
	for i in range(3):
		do_a_flip()
	
	move(West) # pluck fruit
	move(East) # move away again
	
def bamboo_sample_three():
	clear()
	till()
	
	plant(Entities.Bamboo)
	hover(measure()) # hover such that drone will be next to fruit
	print(measure())
	move(East) # move away and wait for it to grow
	for i in range(3):
		do_a_flip()
	
	move(West) # pluck fruit
	hover(measure())
	move(East) # move away again
	
	for i in range(3):
		do_a_flip()
		
	move(West) 
	
def bamboo_sample_four():
	clear()
	till()
	
	plant(Entities.Bamboo)
	
	while True:
	
		ph = 0
		h = 1
		
		while ph != h:
			ph = h
			h = measure()
			print(h)
			hover(h)
			
			move(East) # move away and wait for it to grow
			
			for i in range(4):
				do_a_flip()
				
			move(West) # pluck fruit
		
		move(East)	
		hover(1)
		move(West)
		
def bamboo_row():
	clear()
	
	heights = {}
	
	while True:
		
		x,y = get_pos_x(), get_pos_y()
		
		if get_ground_type() != Grounds.Soil:
				till()
			
		if get_entity_type() != Entities.Bamboo:
				if x % 2 == 0:
					plant(Entities.Bamboo)
		
		if get_entity_type() == Entities.Bamboo:
			h = measure()
			
			previous_height = 0
			if (x,y) in heights:
				previous_height = heights[(x,y)]
			
			# if the plant hasn't grown then we mark it for harvest
			if h == previous_height:
				h = 1
				
			heights[(x,y)] = h
		
		right_x = (x + 1) % get_world_size()
		if (right_x, y) in heights:
			next_height = heights[(right_x, y)]
			# cant hover down if the current one it too tall...
			hover(next_height)
			
		move(East)

heights = {}

def bamboo_cell(x, y):
	global heights
	
	if get_ground_type() != Grounds.Soil:
				till()
			
	if get_entity_type() != Entities.Bamboo:
		if (x % 2 == 0 and y % 2 ==0) or (x % 2 == 1 and y % 2 == 1):
			plant(Entities.Bamboo)
		
	if get_entity_type() == Entities.Bamboo:
		h = measure()
			
		previous_height = 0
		if (x,y) in heights:
			previous_height = heights[(x,y)]
			
		# if the plant hasn't grown then we mark it for harvest
		if h == previous_height:
			h = 1
				
		heights[(x,y)] = h
		
	up_y = (y + 1) % get_world_size()
		
	right_x = x
	if up_y == 0:
		right_x = (x + 1) % get_world_size()
		
	if (right_x, up_y) in heights:
		next_height = heights[(right_x, up_y)]
		hover(next_height)
	
def bamboo_grid():
	clear()
	traverse(bamboo_cell)
	
def bamboo_column():
	while True:
		# use_item(Items.Water)
		i, j = get_pos_x(), get_pos_y()
		bamboo_cell(i, j)
		move(North)
		
def bamboo_parallel():
	clear()
	hover(15)
	for _ in range(get_world_size() - 1):
		if spawn_drone(bamboo_column):
			move(East)
	bamboo_column()

if __name__ == "__main__":
	# set_world_size(4)
	# bamboo_row()
	# bamboo_grid()
	bamboo_parallel()