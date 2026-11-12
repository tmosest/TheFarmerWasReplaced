# https://steamcommunity.com/app/2060160/discussions/0/570428419877172841/
# Much faster but errors out sometimes at if 0 not in etat:
N = get_world_size()
NN = N * N
DESCENTE_MAX = 300
LOT_MIN = 4
P_DESC = 12
MARGE_P = 14
ECART0 = 109
NB = min(max_drones(), N)
uu = []
rr = []
etat = []
num = []
vin = []
sures = []
a_verifier = []
mode = [True]
for y in range(N):
	for x in range(N):
		lst = []
		for yy in range(max(0, y - 1), min(N, y + 2)):
			for xx in range(max(0, x - 1), min(N, x + 2)):
				if xx != x or yy != y:
					lst.append(yy * N + xx)
		vin.append(lst)
		etat.append(0)
		num.append(0)
		uu.append(0)
		rr.append(0)

def move_to(x, y):
	dx = (x - get_pos_x()) % N
	dy = (y - get_pos_y()) % N
	d = East
	if dx > N // 2:
		dx = N - dx
		d = West
	for i in range(dx):
		move(d)
	d = North
	if dy > N // 2:
		dy = N - dy
		d = South
	for i in range(dy):
		move(d)

def aplanir_bande(k):
	ya = (k * N) // NB
	yb = ((k + 1) * N) // NB
	for y in range(ya, yb):
		for i in range(N):
			x = i
			if (y - ya) % 2 == 1:
				x = N - 1 - i
			move_to(x, y)
			n = 0
			while n < DESCENTE_MAX:
				g = get_ground_type()
				if g == Grounds.Dynamite or (g == Grounds.Soot and mode[0]):
					break
				dig()
				n += 1
	return 0

def aplanir_groupe(a, b):
	kids = []
	while b - a > 1:
		mid = (a + b) // 2
		h = spawn_drone(aplanir_groupe, mid, b)
		if h == None:
			break
		kids.append(h)
		b = mid
	for k in range(a, b):
		aplanir_bande(k)
	for h in kids:
		wait_for(h)
	return 0

def classer_sur(j):
	etat[j] = 3
	sures.append(j)
	for k in vin[j]:
		if etat[k] == 1:
			uu[k] -= 1
			if rr[k] >= uu[k]:
				a_verifier.append(k)

def classer_mine(j):
	etat[j] = 2
	for k in vin[j]:
		if etat[k] == 1:
			uu[k] -= 1
			rr[k] -= 1
			if rr[k] <= 0 or rr[k] >= uu[k]:
				a_verifier.append(k)

def enregistrer(c, m):
	avant = etat[c]
	etat[c] = 1
	num[c] = m
	u = 0
	r = m
	for j in vin[c]:
		if etat[j] == 0:
			u += 1
		elif etat[j] == 2:
			r -= 1
	uu[c] = u
	rr[c] = r
	if avant == 0:
		for j in vin[c]:
			if etat[j] == 1:
				uu[j] -= 1
				a_verifier.append(j)
	a_verifier.append(c)

def contrainte(c):
	reste = num[c]
	inc = []
	for j in vin[c]:
		if etat[j] == 0:
			inc.append(j)
		elif etat[j] == 2:
			reste -= 1
	return reste, inc

def propager():
	incoh = 0
	while len(a_verifier) > 0:
		c = a_verifier.pop()
		if etat[c] != 1:
			continue
		u = uu[c]
		rem = rr[c]
		if rem < 0 or rem > u or (u == 0 and rem != 0):
			incoh += 1
		elif u > 0 and rem == 0:
			for j in contrainte(c)[1]:
				classer_sur(j)
		elif u > 0 and rem == u:
			for j in contrainte(c)[1]:
				classer_mine(j)
	return incoh

def sous_ensembles():
	for a in range(NN):
		if etat[a] != 1 or uu[a] < 1:
			continue
		ra, ia = contrainte(a)
		if len(ia) == 0:
			continue
		for v in vin[ia[0]]:
			if v == a or etat[v] != 1 or uu[v] <= uu[a]:
				continue
			rb, ib = contrainte(v)
			dedans = True
			for j in ia:
				if j not in ib:
					dedans = False
			if len(ib) <= len(ia) or not dedans:
				continue
			diff = []
			for j in ib:
				if j not in ia:
					diff.append(j)
			r = rb - ra
			if r == 0 and len(diff) > 0:
				for j in diff:
					if etat[j] == 0:
						classer_sur(j)
			elif r == len(diff) and r > 0:
				for j in diff:
					if etat[j] == 0:
						classer_mine(j)

def choisir_pari():
	risque = []
	for i in range(NN):
		risque.append(-1.0)
	somme = 0
	creuses = 0
	for c in range(NN):
		if etat[c] == 1:
			creuses += 1
			somme += num[c]
			ct = contrainte(c)
			if len(ct[1]) > 0:
				r = ct[0] / len(ct[1])
				for j in ct[1]:
					if r > risque[j]:
						risque[j] = r
	meilleur = -1
	mr = 2.0
	libre = -1
	autre = -1
	for j in range(NN):
		if etat[j] == 0:
			if autre == -1:
				autre = j
			if risque[j] >= 0:
				if risque[j] < mr:
					mr = risque[j]
					meilleur = j
			elif libre == -1:
				libre = j
	if meilleur == -1:
		if libre == -1:
			return autre
		return libre
	if libre != -1 and somme / (8 * creuses) < mr:
		return libre
	return meilleur

def creuser_cases(cases):
	res = []
	for i in cases:
		move_to(i % N, i // N)
		dig()
		if get_ground_type() != Grounds.Soot:
			res.append(-1)
			return res
		m = measure()
		if m == None:
			m = -2
		res.append(m)
	return res

def creuser_groupe(seaux, a, b):
	kids = []
	while b - a > 1:
		mid = (a + b) // 2
		h = spawn_drone(creuser_groupe, seaux, mid, b)
		if h == None:
			break
		kids.append(h)
		b = mid
	out = []
	for k in range(a, b):
		out.append(creuser_cases(seaux[k]))
	for t in range(len(kids) - 1, -1, -1):
		for x in wait_for(kids[t]):
			out.append(x)
	return out

def creuser_lot(cases):
	D = min(NB, len(cases))
	if len(cases) < LOT_MIN or NB <= 1:
		return [cases, creuser_cases(cases)]
	seaux = []
	for g in range(D):
		seaux.append([])
	for i in cases:
		seaux[(i // N * D) // N].append(i)
	out = creuser_groupe(seaux, 0, D)
	ordre = []
	resultats = []
	for g in range(D):
		for t in range(len(out[g])):
			ordre.append(seaux[g][t])
			resultats.append(out[g][t])
	return [ordre, resultats]

def appliquer(ordre, resultats):
	statut = 0
	for t in range(len(resultats)):
		m = resultats[t]
		if m == -1:
			return -1
		if m == -2:
			etat[ordre[t]] = 1
			statut = 1
		else:
			enregistrer(ordre[t], m)
	return statut

def resoudre():
	for c in range(NN):
		etat[c] = 0
		num[c] = 0
		uu[c] = 0
		rr[c] = 0
	while len(sures) > 0:
		sures.pop()
	while len(a_verifier) > 0:
		a_verifier.pop()
	move_to(1, 1)
	dig()
	if get_ground_type() != Grounds.Soot or measure() == None:
		return -1
	enregistrer(N + 1, measure())
	while True:
		if propager() > 0:
			return -1
		if len(sures) == 0:
			sous_ensembles()
			if propager() > 0:
				return -1
		if len(sures) > 0:
			cases = []
			while len(sures) > 0:
				cases.append(sures.pop())
			lot = creuser_lot(cases)
			st = appliquer(lot[0], lot[1])
			if st == -1:
				return 0
			if st == 1:
				return 1
		else:
			if 0 not in etat:
				return 1
			j = choisir_pari()
			r = creuser_cases([j])[0]
			if r == -1:
				return 0
			if r == -2:
				return 1
			enregistrer(j, r)

def descente():
	n = 0
	immobile = 0
	while get_ground_type() != Grounds.Dynamite and n < DESCENTE_MAX and immobile < 3:
		z = get_pos_z()
		dig()
		n += 1
		if get_pos_z() == z:
			immobile += 1
		else:
			immobile = 0
	return get_ground_type() == Grounds.Dynamite

def forer_n(n):
	for i in range(n):
		dig()
	return 0

def descente_para(cible):
	p = min(P_DESC, NB)
	par = (get_pos_z() - cible) // p
	if par < 1:
		return
	aides = []
	for i in range(p - 1):
		w = spawn_drone(forer_n, par)
		if w != None:
			aides.append(w)
	forer_n(par)
	for w in aides:
		wait_for(w)

premier = True
sans = False
zdyn = None
ecart = ECART0
while True:
	if sans:
		z_avant = get_pos_z()
		descente_para(z_avant - ecart + MARGE_P)
		if descente():
			ecart = min(ecart, z_avant - get_pos_z())
		else:
			sans = False
	if not sans:
		clear()
		if premier:
			jump(Unlocks.Dynamite)
			premier = False
		elif zdyn != None:
			descente_para(zdyn - MARGE_P)
		essais = 1
		while not descente() and essais < 4:
			essais += 1
			clear()
		if get_ground_type() != Grounds.Dynamite:
			break
		if zdyn == None or get_pos_z() > zdyn:
			zdyn = get_pos_z()
	mode[0] = not sans
	aplanir_groupe(0, NB)
	verdict = resoudre()
	if verdict == -1:
		break
	sans = True