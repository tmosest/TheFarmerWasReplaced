# https://steamcommunity.com/app/2060160/discussions/0/570428419877172841/
TAILLE = 8
Z_FOND = -60
Z_MIN = -100

if get_world_size() > TAILLE:
	set_world_size(TAILLE)
S = get_world_size()

def go_to(x,y):
	dis = (x - get_pos_x()) % S
	dir = East
	if dis > S / 2:
		dis = S - dis
		dir = West
	for step in range(dis):
		move(dir)
	dis = (y - get_pos_y()) % S
	dir = North
	if dis > S / 2:
		dis = S - dis
		dir = South
	for step in range(dis):
		move(dir)

def reset():
	change_hat(Hats.Gold_Hat)
	clear()
	change_hat(Hats.Mining_Hat)

def dig_one():
	if get_ground_type() == Grounds.Bedrock:
		return False
	for attempt in range(64):
		if dig():
			return True
	return False

def par(task,jobs):
	res = []
	m = max_drones()
	for start in range(0,len(jobs),m):
		stop = min(start + m,len(jobs))
		hs = []
		for q in range(start + 1,stop):
			h = spawn_drone(task,jobs[q])
			if h == None:
				res.append(task(jobs[q]))
			else:
				hs.append(h)
		res.append(task(jobs[start]))
		for h in hs:
			res.append(wait_for(h))
	return res

def forer(n):
	for i in range(n):
		dig()
	return True

def centre():
	go_to(S // 2,S // 2)
	n = (get_pos_z() - Z_FOND) // max_drones()
	if n > 0:
		jobs = []
		for i in range(max_drones()):
			jobs.append(n)
		par(forer,jobs)
	found = False
	while get_ground_type() != Grounds.Limestone:
		if get_ground_type() == Grounds.Sand:
			found = True
		if not found and get_pos_z() <= Z_MIN:
			return False
		if not dig_one():
			return False
	return True

def expose(z):
	while get_pos_z() > z:
		g = get_ground_type()
		if g == Grounds.Sand:
			return True
		if g == Grounds.Limestone or not dig_one():
			return False
	return get_pos_z() == z and get_ground_type() == Grounds.Limestone

def ext(job):
	d, z, px, py = job
	a = East
	b = West
	o = px
	if d == 1:
		a = North
		b = South
		o = py
	go_to(px,py)
	n = 0
	for i in range(S - 1):
		move(a)
		if not expose(z):
			break
		n += 1
	go_to(px,py)
	m = 0
	for i in range(S - 1 - n):
		move(b)
		if not expose(z):
			break
		m += 1
	return d, (o - m) % S, n + m + 1

def prepare(job):
	lo, hi, ox, oy, w, z = job
	go_to(ox,(oy + lo) % S)
	for row in range(lo,hi):
		way = East
		if (row - lo) % 2 == 1:
			way = West
		for i in range(w):
			if not expose(z):
				return False
			if i < w - 1:
				move(way)
		if row < hi - 1:
			move(North)
	return True

def sand(job):
	lo, hi, ox, oy, w, layer, z = job
	width = w - 2 * layer
	go_to((ox + layer) % S,(oy + lo) % S)
	for row in range(lo,hi):
		way = East
		if (row - lo) % 2 == 1:
			way = West
		for i in range(width):
			if get_pos_z() < z or (get_ground_type() != Grounds.Sand and get_ground_type() != Grounds.Limestone):
				return False
			while get_pos_z() < z + layer + 1:
				old = get_pos_z()
				if not place(Grounds.Sand) or get_pos_z() <= old:
					return False
			if i < width - 1:
				move(way)
		if row < hi - 1:
			move(North)
	return True

def bandes(w,layer):
	n = min(w,max_drones())
	res = []
	for i in range(n):
		res.append([layer + w * i // n,layer + w * (i + 1) // n])
	return res

def restore(largeur):
	z = get_pos_z()
	px = get_pos_x()
	py = get_pos_y()
	bounds = {}
	for r in par(ext,[(0,z,px,py),(1,z,px,py)]):
		bounds[r[0]] = r
	ox = bounds[0][1]
	w = bounds[0][2]
	oy = bounds[1][1]
	if w != bounds[1][2] or w % 2 == 0 or (largeur > 0 and w != largeur):
		return False
	jobs = []
	for band in bandes(w,0):
		jobs.append((band[0],band[1],ox,oy,w,z))
	for ok in par(prepare,jobs):
		if ok != True:
			return False
	cx = (ox + w // 2) % S
	cy = (oy + w // 2) % S
	top = z + w // 2 + 1
	go_to(cx,cy)
	while get_pos_z() >= top:
		if get_ground_type() != Grounds.Sand or not dig_one():
			return False
	for layer in range(w // 2):
		jobs = []
		for band in bandes(w - 2 * layer,layer):
			jobs.append((band[0],band[1],ox,oy,w,layer,z))
		for ok in par(sand,jobs):
			if ok != True:
				return False
	go_to(cx,cy)
	while get_pos_z() < top:
		old = get_pos_z()
		if not place(Grounds.Sand):
			return False
		if get_ground_type() == Grounds.Limestone:
			break
		if get_pos_z() <= old:
			return False
	if get_entity_type() != Entities.Sunflower:
		return False
	while not can_harvest():
		if get_entity_type() != Entities.Sunflower:
			return False
	return harvest()

if S >= 5:
	while True:
		reset()
		if centre():
			restore(0)