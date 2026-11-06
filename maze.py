from harvest import bush

def spawn_maze():
	bush()
	use_item(Items.Weird_Substance)
	
def spawn_full_maze(is_new):
	if is_new:
		bush()
	size = get_world_size()
	substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

def traverse_maze():
	print("traversing maze")
	x, y = measure()
	# print("traversing maze to ", x, y)
	
	i = get_pos_x()
	j = get_pos_y()
	pos = (i, j)
	
	queue = []
	queue.append(pos)
	
	routes = {}
	visited = {}
	
	while len(queue) > 0:
		pos = queue.pop()
		
		
		# print(pos)
		# print(queue)
		neighbors = find_links(routes, pos[0], pos[1])
		# print(neighbors)

		for neighbor in neighbors:
			if (neighbor in visited) == False or visited[neighbor] == False:
				queue.append(neighbor)
		
		# prevents loops	
		visited[pos] = True
		# keep a list of routes
		routes[pos] = neighbors
		
	return routes
	
def find_links(routes, i, j):
	# TODO need to move to i, j if I can
	x = get_pos_x()
	y = get_pos_y()
	
	neighbors = []
	
	if x != i or y != j:
		# TODO if these dont match use traversal to find the route
		path = bfs(routes, (x,y), (i,j))
		# print(path)
		moves = convert_path_to_moves(path)
		# print(moves)
		for m in moves:
			move(m)
		# return neighbors
	
	if can_move(North):
		point = (i, j + 1)
		neighbors.append(point)
	if can_move(South):
		point = (i, j - 1)
		neighbors.append(point)
	if can_move(East):
		point = (i + 1, j)
		neighbors.append(point)
	if can_move(West):
		point = (i - 1, j)
		neighbors.append(point)
	return neighbors
	
# Given a graph and initial and destination point it returns a path
# from one to the other like [(0,0), (1,0), (1,1)]
def bfs(routes, init, dest):
	if init == dest:
		return [init]
	
	queue = []
	queue.append(init)
	
	visited = {}
	visited[init] = True
	
	paths = {}
	paths[init] = [init]
	
	while len(queue) > 0:
		pos = queue.pop(0)
		
		neighbors = []
		if pos in routes:
			neighbors = routes[pos]
		# print(neighbors)

		for neighbor in neighbors:
			
			if (neighbor in visited) == False or visited[neighbor] == False:
				queue.append(neighbor)
				
				path = paths[pos]
				new_path = []
				for node in path:
					new_path.append(node)
					
				new_path.append(neighbor)
				paths[neighbor] = new_path 
		
		# prevents loops	
		visited[pos] = True
		
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
	
def solve_maze():
	spawn_full_maze(True)
	
	count = 0
	routes = traverse_maze()
	
	while True:
		x, y = measure()
		print("traversing maze to ", x, y)
		
		i = get_pos_x()
		j = get_pos_y()
		pos = (i, j)
		
		if x != i or y != j:
			# TODO if these dont match use traversal to find the route
			path = bfs(routes, (i,j), (x,y))
			# print(path)
			moves = convert_path_to_moves(path)
			# print(moves)
			for m in moves:
				move(m)
				
		spawn_full_maze(False)
		count = count + 1
		print(count)
	
solve_maze()