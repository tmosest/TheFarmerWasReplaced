# https://steamcommunity.com/app/2060160/discussions/0/824857476142774115/

set_world_size(5)
times_reused=0
substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
def generate_maze():
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)
 
def maze():
	global times_reused
	while True:
		if num_drones() == 25:
			if get_entity_type() == Entities.Treasure:
				if times_reused>=300:
					times_reused=0
					harvest()
					generate_maze()
				else:
					use_item(Items.Weird_Substance, substance)
					times_reused+=1
 
clear()
list = []
 
while num_drones() < 26:
	pos_x = get_pos_x()
	pos_y = get_pos_y()
	current = (pos_x, pos_y)
	if current not in list:
		list.append(current)
		spawn_drone(maze)
		move(North)
	else:
		move(East)
generate_maze()