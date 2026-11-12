from reset_util import *

def hay_avto_start(num):
	clear()
	while True:
		if num_items(Items.Hay) > num:
			break
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			move(North)
		move(East)


def bush_avto_start(num):
	clear()
	
	while True:
		if num_items(Items.Wood) > num:
			break
		for i in range(get_world_size()):
			if can_harvest():
				harvest()
			plant(Entities.Bush)
			move(North)
		move(East)

def tree_avto_start(num):
	while True:
		if num_items(Items.Wood) > num:
			break
		for i in range(get_world_size()):
			for j in range(get_world_size()/2 -1):
				if get_entity_type() == Entities.Tree:
					if can_harvest():
						harvest()
						plant(Entities.Tree)
				else:
					harvest()
					plant(Entities.Tree)
				move(North)
				move(North)
			move(East)
			#move(North)

def carrot_avto_start(num):
	clear()
	while True:
		if num_items(Items.Carrot) > num or num_items(Items.Hay) < 20 or num_items(Items.Wood) < 20:
			break
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if get_ground_type() != Grounds.Soil:
					till() 
				if get_entity_type() == Entities.Carrot:
					if can_harvest():
						harvest()
						plant(Entities.Carrot)
				else:
					plant(Entities.Carrot)
				move(North)
			move(East)


def Weird_avto_start(num):
	clear()
	while True:
		if num_items(Items.Weird_Substance) > num or num_items(Items.Hay) < 20 or num_items(Items.Wood) < 20:
			break
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if can_harvest():
					harvest()
				if get_ground_type() != Grounds.Soil:
					till() 
				if get_entity_type() != Entities.Carrot:
						plant(Entities.Carrot)
						while True:
							if num_items(Items.Fertilizer) > 20:
								break
							else:
								do_a_flip()
						use_item(Items.Fertilizer)
							
				else:
					harvest()
					plant(Entities.Carrot)
					while True:
						if num_items(Items.Fertilizer) > 20:
							break
						else:
							do_a_flip()
					use_item(Items.Fertilizer)
				move(North)
			move(East)
			
			
def find_and_plant_unready(ready_cells):
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if (i, j) in ready_cells:
				continue
			goTo(i, j)
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() == Entities.Pumpkin and can_harvest():
				ready_cells.add((i, j))
			elif get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
				fill_water()
			if len(ready_cells) == get_world_size()**2:
				return True
	return False

def pumpkin_avto_start(num):
	clear()
	while True:
		if num_items(Items.Pumpkin) > num or num_items(Items.Carrot) < 20:
			break
		ready_cells = set()
		all_ready = False
		while not all_ready:
			all_ready = find_and_plant_unready(ready_cells)
		goTo(0, 0)
		harvest()

def cactus_avto_start(num):
	
	clear()

	cache = {}
	
	while True:
		if num_items(Items.Cactus) > num or num_items(Items.Pumpkin) < 20:
			break
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Cactus)
				cache[(i,j)] = measure()
				fill_water()
				move(North)
			move(East)
		
		#sort columns
		for h in range(get_world_size()):
			count = 0
			for i in range(get_world_size() - 1):
				sorted = True
				for s in range(get_world_size() - 1):
					if cache[h,s] > cache[h,s + 1]:
						sorted = False
						break
				if sorted == True:
					break
				for j in range(get_world_size() - count - 1):
					if cache[h,j + 1] < cache[h,j]:
						swap(North)
						cache[(h,j)] = measure()
						cache[(h,j + 1)] = measure(North)
					move(North)
				goTo(h,0)
				count += 1
			move(East)
		
		#sort rows
		for h in range(get_world_size()):
			count = 0
			for i in range(get_world_size() - 1):
				sorted = True
				for s in range(get_world_size() - 1):
					if cache[s,h] > cache[s + 1,h]:
						sorted = False
						break
				if sorted == True:
					break
				for j in range(get_world_size() - count - 1):
					if cache[j + 1,h] < cache[j,h]:
						swap(East)
						cache[(j,h)] = measure()
						cache[(j + 1,h)] = measure(East)
					move(East)
				goTo(0,h)
				count += 1
			move(North)
		
		harvest()

 