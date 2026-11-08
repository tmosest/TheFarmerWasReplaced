# https://github.com/ConnorTheFoolish/CtF_TFWR_Scripts/blob/main/treasureMap
# Cleaned up and refactored some.
# Found a bug when the path connects from one end to the other it can get stuck in an infinite loop
from dig_util import *
from traversal import move_to
				
def vector(cPos,tPos):
	cX,cY = cPos
	tX,tY = tPos
	if cX >= tX:
		h = "R"
	else:
		h = "L"
	if cY >= tY:
		v = "T"
	else:
		v = "B"
	ans = v + h
	return ans

def getPos():
	return (get_pos_x(),get_pos_y())

def newPos(x,y,dir):
	if dir == North:
		why = y + 1
		eks = x
	elif dir == South:
		why = y - 1
		eks = x
	elif dir == East:
		eks = x + 1
		why = y
	elif dir == West:
		eks = x - 1
		why = y
	return (eks,why)

def DFS(endX,endY):
	oppo = {North:South, South:North, East:West, West:East}
	prefer = {"TR":[South,West,North,East], "TL":[South,East,North,West], "BR":[North,West,South,East], "BL":[North,East,South,West]}
	
	endPos = (endX,endY)
	visited = set()
	stack = []
	while getPos() != endPos:
		
		currX,currY = getPos()
		visited.add(getPos())
		
		
		fndNewPath = False
		for direction in prefer[vector(getPos(),endPos)]:
			if (get_ground_type(direction) == Grounds.Treasure_Path) and (get_pos_z(direction) == get_pos_z()):
				nxtX,nxtY = newPos(currX,currY,direction)
				if (nxtX,nxtY) not in visited:
					stack.append(oppo[direction])
					move(direction)
					fndNewPath = True
					break
			
		if not fndNewPath:
			backtrack = stack.pop()
			move(backtrack)

def generate_instructions(path):
	instructions = []
	hori = get_pos_x()
	vert = get_pos_y()
	for i in range(len(path)):
		if path[i] == "D":
			if i != 0:
				instructions.append([hori,vert])
			instructions.append("D")
		elif path[i] == "N":
			vert += 1
		elif path[i] == "S":
			vert -= 1
		elif path[i] == "E":
			hori += 1
		elif path[i] == "W":
			hori -= 1
			
	return instructions
	
def treasure_map(level_after=True):
	dig_parallel_to_ground(Grounds.Basalt)
	move_to(0, 0)
	map = measure()
	move_to(map[0], map[1])
	dig()
	
	path = list(measure())
	instructions = generate_instructions(path)
	
	for i in instructions:
		if i == "D":
			dig()
		else:
			DFS(i[0],i[1])
	harvest()
	
	# clean up
	if level_after:
		z = get_pos_z()
		dig_to_z_parallel(z)
		
				
if __name__ == "__main__":
	clear()
	jump(Unlocks.Treasure_Map)
	while True:
		treasure_map(False)
		while get_ground_type() != Grounds.Basalt:
			move_to(0, 0)
			dig()