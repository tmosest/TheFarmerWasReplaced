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
		
def move_to_center():
	x = get_world_size() / 2
	y = get_world_size() / 2 
	
	if get_world_size() % 2 == 1:
		x = (get_world_size() - 1) / 2
		y = (get_world_size() - 1) / 2
		
	move_to(x, y) 
	
# Given a graph and initial and destination point it returns a path
# from one to the other like [(0,0), (1,0), (1,1)]
def bfs(routes, init, dest):
	if init == dest:
		return [init]
	
	queue = []
	queue.append(init)
	
	visited = set()
	
	paths = {}
	paths[init] = [init]
	
	while len(queue) > 0:
		pos = queue.pop(0)
		# prevents loops	
		visited.add(pos)
		
		neighbors = []
		if pos in routes:
			neighbors = routes[pos]
		# print(neighbors)

		for neighbor in neighbors:
			
			if neighbor not in visited:
				queue.append(neighbor)
				
				path = paths[pos]
				new_path = []
				for node in path:
					new_path.append(node)
					
				new_path.append(neighbor)
				paths[neighbor] = new_path 
				
				if neighbor == dest:
					return paths[dest]
		
	return paths[dest]
	
# Converts [(0,0), (1,0), (1,1)] to [East, North]
def convert_path_to_moves(path):
	moves = []
	
	if len(path) > 1:
		
		for i in range(len(path) - 1):
			dest = path[i + 1]
			init = path[i]
			x = dest[0] - init[0]
			y = dest[1] - init[1]
			
			if x > 0:
				moves.append(East)
			elif x < 0:
				moves.append(West) 
			elif y < 0:
				moves.append(South)
			elif y > 0:
				moves.append(North)
		
	return moves 
