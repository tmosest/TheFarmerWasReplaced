set_world_size(4)

D = {"N": North, "S": South, "E": East, "W": West}

def aller(x, y):
	n = get_world_size()
	dx = (x - get_pos_x()) % n
	dy = (y - get_pos_y()) % n
	d = East
	if dx > n // 2:
		dx = n - dx
		d = West
	for i in range(dx):
		move(d)
	d = North
	if dy > n // 2:
		dy = n - dy
		d = South
	for i in range(dy):
		move(d)

def forer_z(z, x, y):
	aller(x, y)
	while get_pos_z() > z:
		dig()
	return 0

def forer_jusqu(sol, maxi):
	n = 0
	while get_ground_type() != sol and n < maxi:
		dig()
		n += 1
	return get_ground_type() == sol

def sans_boucles(chemin):
	n = get_world_size()
	x = 0
	y = 0
	z = 0
	poss = [(0, 0, 0)]
	pas = []
	index = {}
	index[(0, 0, 0)] = 0
	for l in chemin:
		if l == "N":
			y += 1
		elif l == "S":
			y -= 1
		elif l == "E":
			x += 1
		elif l == "W":
			x -= 1
		else:
			z += 1
		pt = (x % n, y % n, z)
		k = -1
		if pt in index:
			k = index[pt]
		if k >= 0 and k < len(poss) and poss[k] == pt:
			while len(poss) > k + 1:
				poss.pop()
				pas.pop()
		else:
			pas.append(l)
			poss.append(pt)
			index[pt] = len(poss) - 1
	return pas

def chasse(saut):
	clear()
	limite = 200
	if saut:
		jump(Unlocks.Treasure_Map)
		limite = 12
	else:
		x = get_pos_x()
		y = get_pos_y()
		aides = []
		for i in range(11):
			w = spawn_drone(forer_z, -66, x, y)
			if w != None:
				aides.append(w)
		forer_z(-66, x, y)
		for w in aides:
			wait_for(w)
	if not forer_jusqu(Grounds.Basalt, limite):
		return
	pos = measure()
	aller(pos[0], pos[1])
	if not forer_jusqu(Grounds.Treasure_Map, limite):
		return
	for l in sans_boucles(measure()):
		if l == "D":
			dig()
		else:
			move(D[l])
	harvest()

chasse(True)
while True:
	chasse(False)