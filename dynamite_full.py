from traversal import move_to, move_to_center
from dig_util import dig_parallel_to_ground
from dynamite import *

clear()
jump(Unlocks.Dynamite)
dig_parallel_to_ground(Grounds.Dynamite)


# MINESWEEPER SOLVER
# The Farmer Was Replaced
# 32 x 32 mining field

SIZE = 32
TOTAL = SIZE * SIZE

# Tile states
UNKNOWN = 0
SOOT = 1
MINE = 2
SAFE = 3

# Board memory
state = []
numbers = []

for i in range(TOTAL):
	state.append(UNKNOWN)
	numbers.append(0)


# Convert coordinates to array index
def get_index(x, y):
	return x + y * SIZE


# Check board boundaries
def inside(x, y):
	return x >= 0 and x < SIZE and y >= 0 and y < SIZE
	
def calculate_component_probabilities(constraint_cells, constraint_mines):

	frontier = []

	# Collect every unique unknown cell.
	for i in range(len(constraint_cells)):
		for j in range(len(constraint_cells[i])):
			cell = constraint_cells[i][j]

			if cell not in frontier:
				frontier.append(cell)

	frontier_count = len(frontier)

	frequencies = []
	solution_counts = []

	for i in range(frontier_count):
		frequencies.append(0)
		solution_counts.append(0)

	if frontier_count == 0:
		return frontier, frequencies, solution_counts, 1

	# Convert constraint cell IDs into frontier indexes.
	constraint_vars = []

	for i in range(len(constraint_cells)):
		row = []

		for j in range(len(constraint_cells[i])):
			cell = constraint_cells[i][j]
			found = -1

			for k in range(frontier_count):
				if frontier[k] == cell:
					found = k
					break

			row.append(found)

		constraint_vars.append(row)

	# Initially, every frontier cell is its own component.
	component_labels = []

	for i in range(frontier_count):
		component_labels.append(i)

	# Merge cells that appear in the same constraint.
	changed = True

	while changed:
		changed = False

		for i in range(len(constraint_vars)):
			row = constraint_vars[i]

			if len(row) > 1:
				smallest = component_labels[row[0]]

				for j in range(1, len(row)):
					label = component_labels[row[j]]

					if label < smallest:
						smallest = label

				for j in range(len(row)):
					index = row[j]

					if component_labels[index] != smallest:
						component_labels[index] = smallest
						changed = True

	# Solve each independent component.
	for component in range(frontier_count):

		# Only process component representatives.
		if component_labels[component] == component:

			component_vars = []

			for i in range(frontier_count):
				if component_labels[i] == component:
					component_vars.append(i)

			component_size = len(component_vars)

			# Limit exhaustive enumeration to manageable components.
			if component_size > 18:
				return frontier, frequencies, solution_counts, -1

			# Map global frontier indexes to local component indexes.
			local_index = []

			for i in range(frontier_count):
				local_index.append(-1)

			for i in range(component_size):
				global_index = component_vars[i]
				local_index[global_index] = i

			# Calculate the number of possible assignments.
			total_assignments = 1

			for i in range(component_size):
				total_assignments = total_assignments * 2

			assignment = []

			for i in range(component_size):
				assignment.append(0)

			solutions = 0
			mine_frequency = []

			for i in range(component_size):
				mine_frequency.append(0)

			assignment_number = 0

			while assignment_number < total_assignments:

				valid = True

				# Check every constraint belonging to this component.
				for i in range(len(constraint_vars)):

					row = constraint_vars[i]

					if len(row) > 0:

						if component_labels[row[0]] == component:

							mines_found = 0

							for j in range(len(row)):
								local = local_index[row[j]]
								mines_found += assignment[local]

							if mines_found != constraint_mines[i]:
								valid = False
								break

				# Count valid assignments and mine frequencies.
				if valid:

					solutions += 1

					for i in range(component_size):
						if assignment[i] == 1:
							mine_frequency[i] += 1

				# Increment the binary assignment manually.
				position = 0
				carry = 1

				while position < component_size and carry == 1:

					if assignment[position] == 0:
						assignment[position] = 1
						carry = 0
					else:
						assignment[position] = 0
						position += 1

				assignment_number += 1

			# No valid assignments means inconsistent constraints.
			if solutions == 0:
				return frontier, frequencies, solution_counts, 0

			# Store probabilities for each cell in this component.
			for i in range(component_size):

				global_index = component_vars[i]

				frequencies[global_index] = mine_frequency[i]
				solution_counts[global_index] = solutions

	return frontier, frequencies, solution_counts, 1


# Eight neighboring directions
dx = [-1, 0, 1, -1, 1, -1, 0, 1]
dy = [-1, -1, -1, 0, 0, 1, 1, 1]


# INITIAL SAFE DIG
x = get_pos_x()
y = get_pos_y()

start = get_index(x, y)

dig()

state[start] = SOOT
numbers[start] = measure()


# MAIN SOLVER
running = True

while running:

	changed = True
	invalid = False

	# Repeat deductions until no more changes
	while changed and not invalid:

		changed = False

		constraint_cells = []
		constraint_mines = []

		# BUILD CONSTRAINTS
		for y in range(SIZE):
			for x in range(SIZE):

				index = get_index(x, y)

				if state[index] == SOOT:

					cells = []
					known_mines = 0

					for d in range(8):

						nx = x + dx[d]
						ny = y + dy[d]

						if inside(nx, ny):

							ni = get_index(nx, ny)

							if state[ni] == MINE:
								known_mines += 1

							elif state[ni] == UNKNOWN:
								cells.append(ni)

					remaining = numbers[index] - known_mines

					if remaining < 0 or remaining > len(cells):
						invalid = True

					elif len(cells) > 0:

						constraint_cells.append(cells)
						constraint_mines.append(remaining)

					elif remaining != 0:
						invalid = True

		# DIRECT DEDUCTIONS
		for i in range(len(constraint_cells)):

			cells = constraint_cells[i]
			mines = constraint_mines[i]

			if mines == 0:

				for j in range(len(cells)):

					cell = cells[j]

					if state[cell] == UNKNOWN:
						state[cell] = SAFE
						changed = True

			elif mines == len(cells):

				for j in range(len(cells)):

					cell = cells[j]

					if state[cell] == UNKNOWN:
						state[cell] = MINE
						changed = True

		# SUBSET CONSTRAINT DEDUCTIONS
		for i in range(len(constraint_cells)):

			for j in range(len(constraint_cells)):

				if i != j:

					a = constraint_cells[i]
					b = constraint_cells[j]

					# Determine whether A is a subset of B
					subset = True

					for k in range(len(a)):

						found = False

						for m in range(len(b)):

							if a[k] == b[m]:
								found = True

						if not found:
							subset = False

					if subset:

						difference = []

						for k in range(len(b)):

							found = False

							for m in range(len(a)):

								if b[k] == a[m]:
									found = True

							if not found:
								difference.append(b[k])

						mine_difference = (
							constraint_mines[j]
							- constraint_mines[i]
						)

						if mine_difference < 0:
							invalid = True

						elif mine_difference > len(difference):
							invalid = True

						elif mine_difference == 0:

							for k in range(len(difference)):

								cell = difference[k]

								if state[cell] == UNKNOWN:
									state[cell] = SAFE
									changed = True

						elif mine_difference == len(difference):

							for k in range(len(difference)):

								cell = difference[k]

								if state[cell] == UNKNOWN:
									state[cell] = MINE
									changed = True

	# NEVER DIG IF THE CONSTRAINTS ARE INCONSISTENT
	if invalid:
		running = False

	else:

		# FIND A GUARANTEED SAFE TILE
		target = -1

		for i in range(TOTAL):

			if state[i] == SAFE and target == -1:
				target = i

		# NO GUARANTEED SAFE MOVES
		if target == -1:

			frontier, frequencies, solution_counts, status = calculate_component_probabilities(
				constraint_cells,
				constraint_mines
			)
			
			if status != 1:

				running = False
		
			else:
				
				best = -1

				for i in range(len(frontier)):
					if solution_counts[i] > 0:
						if best == -1:
							best = i
						else:
							# Compare probabilities without floating-point division.
							left = frequencies[i] * solution_counts[best]
							right = frequencies[best] * solution_counts[i]
							
							if left < right:
								best = i
								
				if best == -1:

					running = False

				else:

					target = frontier[best]

		else:

			# Convert index back into coordinates
			target_x = target % SIZE
			target_y = target // SIZE

			# Navigate horizontally
			while get_pos_x() < target_x:
				move(East)

			while get_pos_x() > target_x:
				move(West)

			# Navigate vertically
			while get_pos_y() < target_y:
				move(North)

			while get_pos_y() > target_y:
				move(South)

			# Dig only the proven-safe tile
			dig()

			# Record newly revealed soot
			if get_ground_type() == Grounds.Soot:

				state[target] = SOOT
				numbers[target] = measure()

			else:

				# Unexpected result: stop safely
				running = False

