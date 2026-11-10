# https://steamcommunity.com/app/2060160/discussions/0/570428419877172841/
set_world_size(32)
SACRIFICE = 2
N = get_world_size()
M = Grounds.Mushroom
dirs4 = [East, West, North, South]

def inverse(d):
	if d == East:
		return West
	if d == West:
		return East
	if d == North:
		return South
	return North

def move_to(x, y):
	dx = (x - get_pos_x()) % N
	dy = (y - get_pos_y()) % N
	if dx > N // 2:
		for i in range(N - dx):
			move(West)
	else:
		for i in range(dx):
			move(East)
	if dy > N // 2:
		for i in range(N - dy):
			move(South)
	else:
		for i in range(dy):
			move(North)

def vers_champignon():
	n = 0
	while get_ground_type() != M and n < 12:
		dig()
		n += 1
	return get_ground_type() == M

def repartir(f, a, b, s):
	kids = []
	while b - a > 1:
		mid = (a + b) // 2
		h = spawn_drone(repartir, f, mid, b, s)
		if h == None:
			break
		kids.append(h)
		b = mid
	total = 0
	for i in range(a, b):
		total += f(i, s)
	for h in kids:
		total += wait_for(h)
	return total

def descendre(y, zc):
	total = 0
	for x in range(N):
		move_to(x, y)
		while get_ground_type() == M and get_pos_z() > zc - 10:
			dig()
		n = 0
		while get_ground_type() != M and n < 300:
			dig()
			n += 1
		if get_ground_type() == M:
			total += 1
	return total

def plat(y, s):
	for x in range(N):
		move_to(x, y)
		vers_champignon()
	return 0

def visite(tour):
	paires = 0
	m = True
	while m and get_ground_type() == M:
		m = False
		t = measure()
		for d in dirs4:
			if can_push(d) and get_ground_type(d) == M and measure(d) == t:
				push(d)
				paires += 1
				m = True
				break
	if get_ground_type() == M:
		for k in range(4):
			d = dirs4[(get_pos_x() + get_pos_y() + tour + k) % 4]
			if can_push(d):
				push(d)
				break
	return paires

def passer(y, tour):
	total = 0
	for x in range(N):
		move_to(x, y)
		total += visite(tour)
	return total

clear()
jump(Unlocks.Mushrooms)
vers_champignon()
repartir(plat, 0, N, 0)
strate = 1
while True:
	zc = get_pos_z()
	stock0 = num_items(Items.Mushroom)
	for i in range(SACRIFICE):
		move_to((i * N) // SACRIFICE, (i * N) // SACRIFICE)
		dig()
	tour = 0
	paires = 3
	while paires > 2 or tour < 3:
		paires = repartir(passer, 0, N, tour)
		tour += 1
	quick_print("strate", strate, "; gagnes :", num_items(Items.Mushroom) - stock0, "; stock :", num_items(Items.Mushroom))
	if repartir(descendre, 0, N, zc) < N * N // 2:
		break
	move_to(0, 0)
	strate += 1