def initial_till():
	for i in range(get_world_size()):
		for i in range(get_world_size()):
			till()
			move(North)
		move(East)
		
def fill_water():
	while True:
		if get_water() >= 0.7 or num_items(Items.Water) == 0:
			break
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def goTo(xCoord, yCoord):
	if get_pos_x() > xCoord:
		goRight = xCoord + get_world_size() - get_pos_x()
	else:
		goRight = xCoord - get_pos_x()  
		
	if get_pos_x() > xCoord:
		goLeft = get_pos_x() - xCoord
	else:
		goLeft = get_pos_x() + get_world_size() - xCoord
		
	if get_pos_y() > yCoord:
		goUp = yCoord + get_world_size() - get_pos_y()
	else:
		goUp = yCoord - get_pos_y()
		
	if get_pos_y() > yCoord:
		goDown = get_pos_y() - yCoord
	else:
		goDown = get_pos_y() + get_world_size() - yCoord
	

	if goLeft < goRight:
		for a in range(goLeft):
			move(West)
	else:
		for b in range(goRight):
			move(East)
	
	if goDown < goUp:
		for c in range(goDown):
			move(South)
	else:
		for d in range(goUp):
			move(North)

def next_fibonacci_after(n):
	a, b = 0, 1
	while a <= n:
		a, b = b, a + b
	return a

 