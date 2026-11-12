def fertilize_treasure():
	while get_entity_type() == Entities.Treasure:
		substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
		#use_item(Items.Weird_Substance, 200)
		if get_entity_type() == Entities.Treasure:
			harvest()
	return True
 
def complete_maze():

	ix, dirs = 0, [East, South, West, North]
	while get_entity_type() != Entities.Treasure:
		ix += 1 - move(dirs[ix % 4])*2
	tx, ty = measure()

	dest = tx*16 + ty
	fertilize_treasure()
			
	def heu():
		x = get_pos_x()
		y = get_pos_y()        
		if abs(ty - y) < abs(tx - x):
			if x < tx:
				if y < ty:
					return [East, North, South, West]
				else:
					return [East, South, North, West]
			else:
				if y < ty:
					return [West, North, South, East]
				else:
					return [West, South, North, East]
		else:
			if x < tx:
				if y < ty:
					return [North, East, West, South]
				else:
					return [South, East, West, North]
			else:
				if y < ty:
					return [North, West, East, South]
				else:
					return [South, West, East, North]
	
	back = {East: West, South: North, West: East, North: South}

	d = {East: 16, South: -1, West: -16, North: 1}    
	

	while True:
		dead = set()
		chain = set()
		def explore(src, pos):
			if pos == dest:
				return True
			chain.add(pos)
 
			for opt in heu():
				next = pos + d[opt]
				if next not in chain and next not in dead:
					if move(opt):
						if explore(opt, next):
							return True    
						
			dead.add(pos)
			chain.remove(pos)          
			if src != None:
				move(back[src])
		
		explore(None, get_pos_x()*16 + get_pos_y())
		
		dest = measure()
		if dest == None:
			break
		tx, ty = dest
		dest = tx*16 + ty
		
		fertilize_treasure()

 