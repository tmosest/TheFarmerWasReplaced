def grass():
	if can_harvest():
		harvest()
		if get_ground_type() == Grounds.Soil:
			till()
		plant(Entities.Grass)
		
def bush():
	if can_harvest():
		harvest()
		if get_ground_type() == Grounds.Soil:
			till()
		plant(Entities.Bush)

def carrot():
	if can_harvest():
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Carrot)

# Sunflowers need to be picked by pedal size to get the bonus.
def sunflower():
	if can_harvest():
		# measure() # Gets the number of petals
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Sunflower)
		
def tree():
	if can_harvest():
		harvest()
		plant(Entities.Tree)
		# use_item(Items.Water)
		
def pumpkin():
	if can_harvest():
		# measure() # Gets the number of petals
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)
	if get_entity_type() == Entities.Dead_Pumpkin or get_ground_type() == Grounds.Soil:
		plant(Entities.Pumpkin)
		
def cactus():
	if can_harvest():
		# measure() # Gets the number of petals
		harvest()
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Cactus)
				

def catcus_and_weird_substance():
	while True:
		if can_harvest():
			# measure() # Gets the number of petals
			# use_item(Items.Weird_Substance)
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
			use_item(Items.Fertilizer)

def harvest_grass_bush_carrots(i, j):
	if i == 0:
		grass()
	elif i == get_world_size() - 1:
		carrot()
	else:
		bush()
			
def harvest_grass_tree_carrots(i, j):
	if i == 0:
		grass()
	elif i % 2 == 0:
		carrot()
	else:
		tree()
		
def harvest_grass_tree_carrots_sunflower(i, j):
	if i == 0:
		grass()
	elif i % 2 == 0:
		carrot()
	elif i == get_world_size() - 1 and j == get_world_size() - 1:
		sunflower()
	else:
		if j % 2 == 0:
			tree()
		else:
			bush()

def harvest_wood(i, j):
	if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
		tree()
	else:
		bush()
				
def harvest_grass(i, j):
	grass()
	
def harvest_pumpkins(i, j):
	pumpkin()
	
def harvest_cactus(i, j):
	cactus()