from harvest import bush
from traversal import bfs, convert_path_to_moves

def spawn_maze():
	plant(Entities.Bush)
	use_item(Items.Weird_Substance)
	
def spawn_full_maze(is_new):
	if is_new:
		plant(Entities.Bush)
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
	visited = set()
	
	while len(queue) > 0:
		pos = queue.pop()
		# prevents loops	
		visited.add(pos)
		
		
		# print(pos)
		# print(queue)
		neighbors = find_links(routes, pos[0], pos[1])
		# print(neighbors)

		for neighbor in neighbors:
			if neighbor not in visited:
				queue.append(neighbor)
		
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

if __name__ == "__main__":
	clear()
	solve_maze()