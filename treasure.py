from traversal import *
from dig_util import *
from mega_farm import wait_for_drones

# This can take you off the path...
def follow_instructions(instructions):
	for instruction in instructions:
			if instruction == "E":
				move(East)
			elif instruction == "N":
				move(North)
			elif instruction == "S":
				move(South)
			elif instruction == "W":
				move(West)
				
def find_treasure_and_dig_coordinates(instructions, start_pos):
	pos = []
	pos.append(start_pos[0])
	pos.append(start_pos[1])
	
	digs = []
	
	for instruction in instructions:
		if instruction == "E":
			pos[0] = pos[0] + 1
		elif instruction == "N":
			pos[1] = pos[1] + 1
		elif instruction == "S":
			pos[1] = pos[1] - 1
		elif instruction == "W":
			pos[0] = pos[0] - 1
		elif instruction == "D":
			cord = (pos[0], pos[1])
			if cord != start_pos:
				digs.append(cord)
	
	digs.append((pos[0], pos[1]))		
	return digs

# TODO make faster with multiple drones
def generate_graph(path_height):
	move_to(0,0)
	
	graph = {}
	
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			
			x, y, z = get_pos_x(), get_pos_y(), get_pos_z()
			
			if get_ground_type() == Grounds.Treasure_Path:
				neighbors = []
				
				if x + 1 < get_world_size():
					new_pos = (x + 1, y) 
					move(East)
					z = get_pos_z()
					if get_ground_type() == Grounds.Treasure_Path and z == path_height:
						neighbors.append(new_pos)
					move(West)
					
				if y + 1 < get_world_size():
					new_pos = (x, y + 1)
					move(North)
					z = get_pos_z()
					if get_ground_type() == Grounds.Treasure_Path and z == path_height:
						neighbors.append(new_pos)
					move(South)
					
				if x - 1 > -1:
					new_pos = (x - 1, y)
					move(West)
					z = get_pos_z()
					if get_ground_type() == Grounds.Treasure_Path and z == path_height:
						neighbors.append(new_pos)
					move(East)
					
				if y - 1 > -1:
					new_pos = (x, y - 1)
					move(South)
					z = get_pos_z()
					if get_ground_type() == Grounds.Treasure_Path and z == path_height:
						neighbors.append(new_pos)
					move(North)

				graph[(x,y)] = neighbors
			
			move(North)
		move(East)
		
	return graph

# TODO figure out bug
def generate_graph_dp(path_height):
	move_to(0,0)
	
	graph = {}
	not_path = set()
	path = set()
	
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			
			x, y, z = get_pos_x(), get_pos_y(), get_pos_z()
			
			if z != path_height:
				not_path.add((x, y))
			
			elif get_ground_type() != Grounds.Treasure_Path:
				not_path.add((x, y))
			
			elif get_ground_type() == Grounds.Treasure_Path:
				neighbors = []
				
				if x + 1 < get_world_size():
					new_pos = (x + 1, y) 
					if new_pos in path:
						neighbors.append(new_pos)
					elif new_pos not in not_path:
						move(East)
						z = get_pos_z()
						if z != path_height:
							not_path.add(new_pos)
						elif get_ground_type() == Grounds.Treasure_Path:
							neighbors.append(new_pos)
							path.add(new_pos)
						else:
							not_path.add(new_pos)
						move(West)
					
				if y + 1 < get_world_size():
					new_pos = (x, y + 1)
					if new_pos in path:
						neighbors.append(new_pos)
					elif new_pos not in not_path:
						move(North)
						if z != path_height:
							not_path.add(new_pos)
						elif get_ground_type() == Grounds.Treasure_Path:
							neighbors.append(new_pos)
							path.add(new_pos)
						else:
							not_path.add(new_pos)
						move(South)
					
				if x - 1 > -1:
					new_pos = (x - 1, y)
					if new_pos in path:
						neighbors.append(new_pos)
					elif (x - 1, y) not in not_path:
						move(West)
						if z != path_height:
							not_path.add(new_pos)
						elif get_ground_type() == Grounds.Treasure_Path:
							neighbors.append(new_pos)
							path.add(new_pos)
						else:
							not_path.add(new_pos)
						move(East)
					
				if y - 1 > -1:
					new_pos = (x, y - 1)
					if new_pos in path:
						neighbors.append(new_pos)
					elif new_pos not in not_path:
						move(South)
						if z != path_height:
							not_path.add(new_pos)
						elif get_ground_type() == Grounds.Treasure_Path:
							neighbors.append(new_pos)
							path.add(new_pos)
						else:
							not_path.add(new_pos)
						move(North)

				graph[(x,y)] = neighbors
			
			move(North)
		move(East)
		
	return graph
	
def find_treasure(dig_positions):
	z = get_pos_z()
	drone = spawn_drone(generate_graph, z)
	graph = wait_for(drone)
	
	# Need to handle dig spots
	for i in range(len(dig_positions) - 1):
		x, y = get_pos_x(), get_pos_y()
		start_pos = (x, y)
		end_pos = dig_positions[i]
	
		path = bfs(graph, start_pos, end_pos)
		moves = convert_path_to_moves(path)
		for m in moves:
			move(m)
			
		dig()
		
		z = get_pos_z()
		drone = spawn_drone(generate_graph, z)
		graph = wait_for(drone)
		
	x, y = get_pos_x(), get_pos_y()
	start_pos = (x, y)
	end_pos = dig_positions[len(dig_positions) - 1]
	
	path = bfs(graph, start_pos, end_pos)
	moves = convert_path_to_moves(path)
	for m in moves:
		move(m)
	
def hunt_treasure():
	positions = dig_and_search_parallel(Grounds.Basalt)
	
	# Measuring the basalt returns the position of the treasure map
	pos = (0,0)
	for p in positions:
		pos = p
		break
	move_to(pos[0], pos[1])
	map_pos = measure()
	
	# Move to the map position
	move_to(map_pos[0], map_pos[1])
	
	while get_ground_type() != Grounds.Treasure_Map:
		dig()
		
	instructions = measure()
	# print("instructions: ", instructions)

	# Dig into the map to start the treasure hunt
	dig()
	
	# Follow the instructions
	
	# This can take you off the path...
	# follow_instructions(instructions)
	
	# This just generates the final coordinates instead
	dig_positions = find_treasure_and_dig_coordinates(instructions, map_pos)
	print("Treasure at ", dig_positions)
	
	find_treasure(dig_positions)
			
	# We found the treasure and can harvest it
	if get_entity_type() == Entities.Underground_Treasure:
		harvest()

if __name__ == "__main__":
	clear()
	set_world_size(5)
	jump(Unlocks.Treasure_Map)
	hunt_treasure()