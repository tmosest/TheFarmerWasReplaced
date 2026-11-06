from harvest import grass, bush, tree, carrot
from traversal import move_to

def harvest_with_companions():
	clear()
	# Plant something
	grass()
	(i, j) = get_pos_x(), get_pos_y()
	
	queue = []
	queue.append((i,j))
	
	while True:
		
		pos = queue.pop(0)
		
		move_to(pos[0], pos[1])
		
		plant_type, (x, y) = get_companion()
		# print(plant_type, (x, y))
		move_to(x, y)
		
		if plant_type == Entities.Bush:
			bush()
		elif plant_type == Entities.Carrot:
			carrot()
		elif plant_type == Entities.Tree:
			tree()
		elif plant_type == Entities.Grass:
			grass()
			
		move_to(pos[0], pos[1])
		
		while can_harvest() == False:
			do_a_flip()
		harvest()
		
		queue.append((x,y))
		
	