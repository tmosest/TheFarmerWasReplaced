def for_all(f):
	def row():
		for _ in range(get_world_size()-1):
			f()
			move(East)
		f()
	for _ in range(get_world_size()):
		if not spawn_drone(row):
			row()
		move(North)
		
def for_all_c(f):
	def row():
		while True:
			f()
			move(East)
		f()
	while True:
		if not spawn_drone(row):
			row()
		move(North)
		move(East)
		move(East)

def for_all_T(f):
	def row():
		for _ in range(100*get_world_size()-1):
			f()
	for _ in range(get_world_size()):
		if not spawn_drone(row):
			row()
		move(North)
		move(East)
		move(East)

def for_all_long(f):
	def row():
		while True:
			f()
			move(East)
		f()
	while True:
		if num_drones() <= max_drones()/2:
			if not spawn_drone(row):
				row()
		move(North)
		move(North)
		move(North)

 