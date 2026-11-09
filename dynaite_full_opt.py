# Tried to update dynamite_full to run faster but this appears to fail more...
from traversal import move_to, move_to_center
from dig_util import dig_parallel_to_ground

# ==========================================
# MINESWEEPER SOLVER
# The Farmer Was Replaced
# Parallel drone implementation
# ==========================================

SIZE = get_world_size()
TOTAL = SIZE * SIZE

UNKNOWN = 0
SOOT = 1
MINE = 2
SAFE = 3

WORKERS = 8
MAX_DRONES = 31
MAX_COMPONENT_SIZE = 18

dx = [-1, 0, 1, -1, 1, -1, 0, 1]
dy = [-1, -1, -1, 0, 0, 1, 1, 1]

state = []
numbers = []

for i in range(TOTAL):
	state.append(UNKNOWN)
	numbers.append(0)


# ==========================================
# GENERAL HELPERS
# ==========================================

def get_index(x, y):
	return x + y * SIZE


def inside(x, y):
	if x < 0:
		return False

	if y < 0:
		return False

	if x >= SIZE:
		return False

	if y >= SIZE:
		return False

	return True


def contains_cell(cells, cell):

	for i in range(len(cells)):
		if cells[i] == cell:
			return True

	return False


def same_cells(a, b):

	if len(a) != len(b):
		return False

	for i in range(len(a)):
		if not contains_cell(b, a[i]):
			return False

	return True


def is_subset(a, b):

	if len(a) > len(b):
		return False

	for i in range(len(a)):
		if not contains_cell(b, a[i]):
			return False

	return True


def difference_cells(a, b):

	result = []

	for i in range(len(a)):

		if not contains_cell(b, a[i]):
			result.append(a[i])

	return result


def add_constraint(cells_list, mines_list, cells, mines):

	for i in range(len(cells_list)):

		if same_cells(cells_list[i], cells):

			if mines_list[i] != mines:
				return -1

			return 0

	cells_list.append(cells)
	mines_list.append(mines)

	return 1

# ==========================================
# INCREMENTAL CONSTRAINT STATE
# ==========================================

# Cached constraint for each revealed clue.
clue_cells = []
clue_mines = []
clue_active = []

# Clues requiring recalculation.
dirty_clues = []
dirty_flags = []

# Cells whose states have changed.
changed_cells = []

for i in range(TOTAL):

	clue_cells.append([])
	clue_mines.append(0)
	clue_active.append(0)

	dirty_flags.append(0)

def mark_cell_changed(cell):

	if not contains_cell(changed_cells, cell):
		changed_cells.append(cell)

def mark_dirty_clue(cell):

	if state[cell] != SOOT:
		return

	if dirty_flags[cell] == 0:

		dirty_flags[cell] = 1
		dirty_clues.append(cell)


def mark_affected_clues(cell):

	x = cell % SIZE
	y = cell // SIZE

	# The changed cell might itself be a revealed clue.
	mark_dirty_clue(cell)

	for d in range(8):

		nx = x + dx[d]
		ny = y + dy[d]

		if inside(nx, ny):

			neighbor = get_index(nx, ny)

			mark_dirty_clue(neighbor)

active_clues = []


def remove_active_clue(clue):

	for i in range(len(active_clues)):

		if active_clues[i] == clue:

			active_clues.pop(i)
			return


def update_clue_constraint(clue):

	unknown = []
	known_mines = 0

	x = clue % SIZE
	y = clue // SIZE

	for d in range(8):

		nx = x + dx[d]
		ny = y + dy[d]

		if inside(nx, ny):

			neighbor = get_index(nx, ny)

			if state[neighbor] == UNKNOWN:

				unknown.append(neighbor)

			elif state[neighbor] == MINE:

				known_mines += 1

	remaining = numbers[clue] - known_mines

	# Validate the constraint.
	if remaining < 0:
		return -1

	if remaining > len(unknown):
		return -1

	# No unknown neighbors remain.
	if len(unknown) == 0:

		if remaining != 0:
			return -1

		clue_cells[clue] = []
		clue_mines[clue] = 0

		if clue_active[clue] == 1:

			clue_active[clue] = 0
			remove_active_clue(clue)

		return 1

	# Update cached constraint.
	clue_cells[clue] = unknown
	clue_mines[clue] = remaining

	if clue_active[clue] == 0:

		clue_active[clue] = 1
		active_clues.append(clue)

	return 1

# ==========================================
# ZERO EXPANSION
# ==========================================

zero_queue = []
zero_processed = []

for i in range(TOTAL):
	zero_processed.append(0)

def register_zero(cell):

	if numbers[cell] == 0 and zero_processed[cell] == 0:

		zero_queue.append(cell)
		zero_processed[cell] = 1

def expand_zero_queue():

	expanded = False

	while len(zero_queue) > 0:

		cell = zero_queue.pop(0)

		x = cell % SIZE
		y = cell // SIZE

		for d in range(8):

			nx = x + dx[d]
			ny = y + dy[d]

			if inside(nx, ny):

				neighbor = get_index(nx, ny)

				if state[neighbor] == UNKNOWN:

					state[neighbor] = SAFE
					mark_cell_changed(neighbor)

					expanded = True

	return expanded

def dig_zero_regions():

	while True:

		expanded = expand_zero_queue()

		dug = dig_safe_cells_parallel()

		if dug == -1:
			return -1

		if not expanded and dug == 0:
			return 1

# ==========================================
# PARALLEL SCANNING
# ==========================================

worker_state = []
worker_numbers = []
worker_start = 0
worker_end = 0

def dig_worker_batch(targets):

	pending = []

	for i in range(len(targets)):
		pending.append(targets[i])

	results = []
	complete = 0

	while len(pending) > 0:

		# Find the nearest remaining cell.
		best_index = 0
		best_distance = 999999

		x = get_pos_x()
		y = get_pos_y()

		for i in range(len(pending)):

			cell = pending[i]

			target_x = cell % SIZE
			target_y = cell // SIZE

			distance = abs(target_x - x) + abs(target_y - y)

			if distance < best_distance:

				best_distance = distance
				best_index = i

		target = pending[best_index]

		# Move and dig.
		move_to_cell(target)
		dig()

		number = measure()

		results.append([target, number])

		# None means all dynamite has been found.
		if number == None:

			complete = 1
			break

		# Remove completed target.
		next_pending = []

		for i in range(len(pending)):

			if i != best_index:
				next_pending.append(pending[i])

		pending = next_pending

	return [results, complete]
	
def dig_safe_cells_parallel():

	safe_cells = []

	for cell in range(TOTAL):

		if state[cell] == SAFE:
			safe_cells.append(cell)

	if len(safe_cells) == 0:
		return 0

	# Total workers, including coordinator.
	total_slots = max_drones()

	if total_slots < 1:
		total_slots = 1

	if total_slots > MAX_DRONES + 1:
		total_slots = MAX_DRONES + 1

	worker_count = len(safe_cells)

	if worker_count > total_slots:
		worker_count = total_slots

	# Create batches.
	batches = []

	for i in range(worker_count):
		batches.append([])

	for i in range(len(safe_cells)):

		batch = i % worker_count

		batches[batch].append(safe_cells[i])

	drones = []
	main_targets = batches[0]

	# Spawn workers for all batches except the coordinator.
	for i in range(1, worker_count):

		drone = spawn_drone(dig_worker_batch, batches[i])

		if drone != None:

			drones.append(drone)

		else:

			# If spawning fails, the coordinator handles
			# the unassigned batch.
			for j in range(len(batches[i])):
				main_targets.append(batches[i][j])

	# Coordinator digs simultaneously with the other drones.
	main_result = dig_worker_batch(main_targets)

	all_results = []
	all_results.append(main_result)

	# Collect worker results.
	for i in range(len(drones)):

		result = wait_for(drones[i])

		all_results.append(result)

	# Update board state.
	dug_count = 0
	complete = 0

	for i in range(len(all_results)):

		result = all_results[i]

		dig_results = result[0]

		if result[1] == 1:
			complete = 1

		for j in range(len(dig_results)):

			target = dig_results[j][0]
			number = dig_results[j][1]

			state[target] = SOOT
			numbers[target] = number

			mark_cell_changed(target)
			register_zero(target)

			dug_count += 1

			if number == None:
				complete = 1

	if complete:
		return -1

	return dug_count


def scan_constraints_worker():

	cells_result = []
	mines_result = []

	error = 0

	for index in range(worker_start, worker_end):

		if worker_state[index] == SOOT:

			x = index % SIZE
			y = index // SIZE

			unknown = []
			known_mines = 0

			for d in range(8):

				nx = x + dx[d]
				ny = y + dy[d]

				if inside(nx, ny):

					neighbor = get_index(nx, ny)
					value = worker_state[neighbor]

					if value == UNKNOWN:
						unknown.append(neighbor)

					elif value == MINE:
						known_mines += 1

			remaining = worker_numbers[index] - known_mines

			if remaining < 0:
				error = 1

			elif remaining > len(unknown):
				error = 1

			elif len(unknown) > 0:

				cells_result.append(unknown)
				mines_result.append(remaining)

			elif remaining != 0:

				error = 1

	return [cells_result, mines_result, error]


def build_constraints_parallel():

	global worker_state
	global worker_numbers
	global worker_start
	global worker_end

	constraint_cells = []
	constraint_mines = []

	workers = WORKERS

	if workers > MAX_DRONES:
		workers = MAX_DRONES

	chunk_size = TOTAL // workers

	drones = []

	# Launch workers.
	for i in range(workers):

		worker_state = state
		worker_numbers = numbers

		worker_start = i * chunk_size

		if i == workers - 1:
			worker_end = TOTAL
		else:
			worker_end = (i + 1) * chunk_size

		drone = spawn_drone(scan_constraints_worker)

		drones.append(drone)

	# Collect results.
	for i in range(len(drones)):

		result = wait_for(drones[i])

		cells = result[0]
		mines = result[1]
		error = result[2]

		if error == 1:
			return constraint_cells, constraint_mines, -1

		for j in range(len(cells)):

			constraint_cells.append(cells[j])
			constraint_mines.append(mines[j])

	return constraint_cells, constraint_mines, 1

def build_constraints_incremental():

	global changed_cells
	global dirty_clues

	# Mark affected clues.
	for i in range(len(changed_cells)):

		cell = changed_cells[i]

		mark_affected_clues(cell)

	changed_cells = []

	# Update only dirty constraints.
	for i in range(len(dirty_clues)):

		clue = dirty_clues[i]

		result = update_clue_constraint(clue)

		if result == -1:
			return [], [], -1

		dirty_flags[clue] = 0

	dirty_clues = []

	# Return active cached constraints.
	constraint_cells = []
	constraint_mines = []

	for i in range(len(active_clues)):

		clue = active_clues[i]

		constraint_cells.append(clue_cells[clue])
		constraint_mines.append(clue_mines[clue])

	return constraint_cells, constraint_mines, 1

# ==========================================
# PARALLEL SUBSET DEDUCTION
# ==========================================

subset_worker_cells = []
subset_worker_mines = []
subset_worker_index = []
subset_worker_start = 0
subset_worker_end = 0

def build_constraint_index(constraint_cells):

	index = []

	for i in range(TOTAL):
		index.append([])

	for i in range(len(constraint_cells)):

		cells = constraint_cells[i]

		for j in range(len(cells)):

			cell = cells[j]

			index[cell].append(i)

	return index

def subset_deduction_worker():

	derived_cells = []
	derived_mines = []

	safe_cells = []
	mine_cells = []

	error = 0

	count = len(subset_worker_cells)

	# Candidate deduplication markers.
	# Avoids repeatedly comparing candidate IDs.
	candidate_seen = []

	for i in range(count):
		candidate_seen.append(-1)

	for i in range(subset_worker_start, subset_worker_end):

		a = subset_worker_cells[i]
		mines_a = subset_worker_mines[i]

		# ----------------------------------
		# Direct deductions.
		# ----------------------------------

		if mines_a < 0 or mines_a > len(a):

			error = 1

		elif mines_a == 0:

			for j in range(len(a)):

				if not contains_cell(safe_cells, a[j]):
					safe_cells.append(a[j])

		elif mines_a == len(a):

			for j in range(len(a)):

				if not contains_cell(mine_cells, a[j]):
					mine_cells.append(a[j])

		# ----------------------------------
		# Find only overlapping constraints.
		# ----------------------------------

		candidates = []

		for j in range(len(a)):

			cell = a[j]

			related = subset_worker_index[cell]

			for k in range(len(related)):

				other = related[k]

				# Only process each pair once.
				if other <= i:
					continue

				# Avoid duplicate candidates.
				if candidate_seen[other] != i:

					candidate_seen[other] = i
					candidates.append(other)

		# ----------------------------------
		# Compare candidate constraints.
		# ----------------------------------

		for j in range(len(candidates)):

			other = candidates[j]

			b = subset_worker_cells[other]
			mines_b = subset_worker_mines[other]

			# A cannot be a subset of B if it is larger.
			if len(a) <= len(b):

				if is_subset(a, b):

					difference = difference_cells(b, a)
					remaining = mines_b - mines_a

					if remaining < 0:
						error = 1

					elif remaining > len(difference):
						error = 1

					elif len(difference) > 0:

						derived_cells.append(difference)
						derived_mines.append(remaining)

			# B cannot be a subset of A if it is larger.
			if len(b) <= len(a):

				if is_subset(b, a):

					difference = difference_cells(a, b)
					remaining = mines_a - mines_b

					if remaining < 0:
						error = 1

					elif remaining > len(difference):
						error = 1

					elif len(difference) > 0:

						derived_cells.append(difference)
						derived_mines.append(remaining)

	return [
		derived_cells,
		derived_mines,
		safe_cells,
		mine_cells,
		error
	]


def close_constraints_parallel(constraint_cells, constraint_mines):

	global subset_worker_cells
	global subset_worker_mines
	global subset_worker_index
	global subset_worker_start
	global subset_worker_end

	stable = False

	safe_cells = []
	mine_cells = []

	while not stable:

		count = len(constraint_cells)

		subset_worker_index = build_constraint_index(constraint_cells)

		if count == 0:
			stable = True
			break

		workers = 1

		if count >= 40:
			workers = 2

		if count >= 100:
			workers = 4

		if count >= 250:
			workers = 8

		if workers > MAX_DRONES:
			workers = MAX_DRONES

		if workers > count:
			workers = count

		results = []

		# Single-worker fast path.
		if workers == 1:

			subset_worker_cells = constraint_cells
			subset_worker_mines = constraint_mines

			subset_worker_start = 0
			subset_worker_end = count

			result = subset_deduction_worker()

			if result != None:
				results.append(result)

		else:

			chunk_size = count // workers
			drones = []

			# Spawn all workers before waiting.
			for i in range(workers):

				subset_worker_cells = constraint_cells
				subset_worker_mines = constraint_mines

				subset_worker_start = i * chunk_size

				if i == workers - 1:
					subset_worker_end = count
				else:
					subset_worker_end = (i + 1) * chunk_size

				drone = spawn_drone(subset_deduction_worker)

				if drone != None:
					drones.append(drone)

			# Collect results after spawning.
			for i in range(len(drones)):

				result = wait_for(drones[i])

				if result != None:
					results.append(result)

		new_count = 0

		safe_cells = []
		mine_cells = []

		# Merge worker results.
		for i in range(len(results)):

			result = results[i]

			derived_cells = result[0]
			derived_mines = result[1]

			worker_safe = result[2]
			worker_mines = result[3]

			error = result[4]

			if error == 1:
				return constraint_cells, constraint_mines, safe_cells, mine_cells, -1

			for j in range(len(worker_safe)):

				if not contains_cell(safe_cells, worker_safe[j]):
					safe_cells.append(worker_safe[j])

			for j in range(len(worker_mines)):

				if not contains_cell(mine_cells, worker_mines[j]):
					mine_cells.append(worker_mines[j])

			for j in range(len(derived_cells)):

				added = add_constraint(
					constraint_cells,
					constraint_mines,
					derived_cells[j],
					derived_mines[j]
				)

				if added == -1:
					return constraint_cells, constraint_mines, safe_cells, mine_cells, -1

				if added == 1:
					new_count += 1

		# Check contradictory deductions.
		for i in range(len(safe_cells)):

			if contains_cell(mine_cells, safe_cells[i]):
				return constraint_cells, constraint_mines, safe_cells, mine_cells, -1

		if new_count == 0:
			stable = True

		if len(constraint_cells) > 2000:
			return constraint_cells, constraint_mines, safe_cells, mine_cells, -1

	return constraint_cells, constraint_mines, safe_cells, mine_cells, 1


# ==========================================
# COMPONENT PROBABILITY WORKER
# Constraint-pruned backtracking
# ==========================================

component_worker_size = 0
component_worker_constraints = []
component_worker_mines = []


def search_component(assignment, size, constraints, required, frequencies, stats, degrees):

	changed = []
	valid = True
	propagated = True

	# --------------------------------------
	# 1. Constraint propagation
	# --------------------------------------

	while propagated and valid:

		propagated = False

		for i in range(len(constraints)):

			row = constraints[i]
			target = required[i]

			assigned_mines = 0
			unknown_count = 0

			for j in range(len(row)):

				value = assignment[row[j]]

				if value == 1:
					assigned_mines += 1

				elif value == -1:
					unknown_count += 1

			# Impossible constraint.
			if assigned_mines > target:
				valid = False
				break

			if assigned_mines + unknown_count < target:
				valid = False
				break

			# Determine whether remaining variables are forced.
			if unknown_count > 0:

				forced_value = -1

				if assigned_mines == target:
					forced_value = 0

				elif assigned_mines + unknown_count == target:
					forced_value = 1

				if forced_value != -1:

					for j in range(len(row)):

						variable = row[j]

						if assignment[variable] == -1:

							assignment[variable] = forced_value
							changed.append(variable)
							propagated = True

	# --------------------------------------
	# 2. Explore if still valid
	# --------------------------------------

	if valid:

		# Choose the unassigned variable with
		# the highest constraint occurrence.
		best_variable = -1
		best_degree = -1

		for variable in range(size):

			if assignment[variable] == -1:

				if degrees[variable] > best_degree:

					best_degree = degrees[variable]
					best_variable = variable

		# ----------------------------------
		# 3. Complete assignment found
		# ----------------------------------

		if best_variable == -1:

			stats[0] += 1

			for i in range(size):

				if assignment[i] == 1:
					frequencies[i] += 1

		else:

			# ----------------------------------
			# 4. Branch: assume safe
			# ----------------------------------

			assignment[best_variable] = 0

			search_component(
				assignment,
				size,
				constraints,
				required,
				frequencies,
				stats,
				degrees
			)

			# ----------------------------------
			# 5. Branch: assume mine
			# ----------------------------------

			assignment[best_variable] = 1

			search_component(
				assignment,
				size,
				constraints,
				required,
				frequencies,
				stats,
				degrees
			)

			assignment[best_variable] = -1

	# --------------------------------------
	# 6. Undo propagation
	# --------------------------------------

	for i in range(len(changed)):
		assignment[changed[i]] = -1


def solve_component_worker():

	size = component_worker_size

	assignment = []
	frequencies = []
	degrees = []

	# Initialize arrays.
	for i in range(size):

		assignment.append(-1)
		frequencies.append(0)
		degrees.append(0)

	# Calculate variable degrees once.
	for i in range(len(component_worker_constraints)):

		row = component_worker_constraints[i]

		for j in range(len(row)):

			degrees[row[j]] += 1

	stats = [0]

	search_component(
		assignment,
		size,
		component_worker_constraints,
		component_worker_mines,
		frequencies,
		stats,
		degrees
	)

	return [frequencies, stats[0]]


# ==========================================
# CONNECTED COMPONENT PROBABILITIES
# ==========================================

def calculate_component_probabilities(constraint_cells, constraint_mines):

	global component_worker_size
	global component_worker_constraints
	global component_worker_mines

	frontier = []

	# Build unique frontier.
	for i in range(len(constraint_cells)):

		for j in range(len(constraint_cells[i])):

			cell = constraint_cells[i][j]

			if not contains_cell(frontier, cell):
				frontier.append(cell)

	frontier_count = len(frontier)

	frequencies = []
	solution_counts = []

	for i in range(frontier_count):

		frequencies.append(0)
		solution_counts.append(0)

	if frontier_count == 0:
		return frontier, frequencies, solution_counts, 1

	# Convert constraints into frontier indexes.
	constraint_vars = []

	for i in range(len(constraint_cells)):

		row = []

		for j in range(len(constraint_cells[i])):

			found = -1

			for k in range(frontier_count):

				if frontier[k] == constraint_cells[i][j]:
					found = k
					break

			row.append(found)

		constraint_vars.append(row)

	# Build connected components.
	component_labels = []

	for i in range(frontier_count):
		component_labels.append(i)

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

	# Prepare independent component tasks.
	task_cells = []
	task_constraints = []
	task_mines = []

	for component in range(frontier_count):

		if component_labels[component] == component:

			component_vars = []

			for i in range(frontier_count):

				if component_labels[i] == component:
					component_vars.append(i)

			component_size = len(component_vars)

			if component_size > MAX_COMPONENT_SIZE:

				return frontier, frequencies, solution_counts, -1

			# Map frontier indexes to local component indexes.
			local_index = []

			for i in range(frontier_count):
				local_index.append(-1)

			for i in range(component_size):

				global_index = component_vars[i]
				local_index[global_index] = i

			component_constraints = []
			component_mines_list = []

			for i in range(len(constraint_vars)):

				row = constraint_vars[i]

				if len(row) > 0:

					if component_labels[row[0]] == component:

						local_row = []

						for j in range(len(row)):
							local_row.append(local_index[row[j]])

						component_constraints.append(local_row)
						component_mines_list.append(constraint_mines[i])

			task_cells.append(component_vars)
			task_constraints.append(component_constraints)
			task_mines.append(component_mines_list)

	# Execute component workers in batches.
	task_count = len(task_cells)
	task_start = 0

	while task_start < task_count:

		batch_size = task_count - task_start

		if batch_size > MAX_DRONES:
			batch_size = MAX_DRONES

		drones = []

		for i in range(batch_size):

			task = task_start + i

			component_worker_size = len(task_cells[task])
			component_worker_constraints = task_constraints[task]
			component_worker_mines = task_mines[task]

			drone = spawn_drone(solve_component_worker)

			drones.append(drone)

		# Collect results.
		for i in range(batch_size):

			task = task_start + i

			result = wait_for(drones[i])

			mine_frequency = result[0]
			solutions = result[1]

			if solutions == 0:

				return frontier, frequencies, solution_counts, 0

			for j in range(len(task_cells[task])):

				global_index = task_cells[task][j]

				frequencies[global_index] = mine_frequency[j]
				solution_counts[global_index] = solutions

		task_start += batch_size

	return frontier, frequencies, solution_counts, 1


# ==========================================
# MOVEMENT
# ==========================================

def move_to_cell(target):

	target_x = target % SIZE
	target_y = target // SIZE

	while get_pos_x() < target_x:
		move(East)

	while get_pos_x() > target_x:
		move(West)

	while get_pos_y() < target_y:
		move(North)

	while get_pos_y() > target_y:
		move(South)

def dynamite_full():
	global state
	global numbers
	
	global clue_cells
	global clue_mines
	global clue_active
	
	global dirty_clues
	global dirty_flags

	global changed
	global changed_cells

	global active_clues
	global worker_state
	global worker_numbers
	global worker_start
	global worker_end
	global subset_worker_cells
	global subset_worker_mines
	global subset_worker_index
	global subset_worker_start
	global subset_worker_end
	global component_worker_size
	global component_worker_constraints
	global component_worker_mines

	global zero_queue
	global zero_processed

	dig_parallel_to_ground(Grounds.Dynamite)
	# ==========================================
	# RESET GLOBAL STATE
	# ==========================================

	state = []
	numbers = []

	for i in range(TOTAL):
		state.append(UNKNOWN)
		numbers.append(0)

	# Cached constraint for each revealed clue.
	clue_cells = []
	clue_mines = []
	clue_active = []

	# Clues requiring recalculation.
	dirty_clues = []
	dirty_flags = []

	for i in range(TOTAL):
		clue_cells.append([])
		clue_mines.append(0)
		clue_active.append(0)
	
		dirty_flags.append(0)


	# Cells whose states have changed.
	changed_cells = []

	active_clues = []
	worker_state = []
	worker_numbers = []
	worker_start = 0
	worker_end = 0
	subset_worker_cells = []
	subset_worker_mines = []
	subset_worker_index = []
	subset_worker_start = 0
	subset_worker_end = 0
	component_worker_size = 0
	component_worker_constraints = []
	component_worker_mines = []

	for i in range(TOTAL):
		clue_cells.append([])
		clue_mines.append(0)
		clue_active.append(0)
	
		dirty_flags.append(0)
	
		for i in range(TOTAL):
			state.append(UNKNOWN)
			numbers.append(0)

	zero_queue = []
	zero_processed = []

	for i in range(TOTAL):
		zero_processed.append(0)

	for i in range(TOTAL):

		clue_cells.append([])
		clue_mines.append(0)
		clue_active.append(0)

		dirty_flags.append(0)

	for i in range(TOTAL):
		state.append(UNKNOWN)
		numbers.append(0)

	# ==========================================
	# STARTING TILE
	# ==========================================
	
	start = get_index(get_pos_x(), get_pos_y())
	
	dig()
	
	state[start] = SOOT
	numbers[start] = measure()
	register_zero(start)

	mark_cell_changed(start)

	running = True
	
	if numbers[start] == None:
		running = False

	# ==========================================
	# MAIN SOLVER
	# ==========================================
	
	while running:


		# --------------------------------------
		# 1. Scan the board in parallel.
		# --------------------------------------

		# Expand all discovered zero regions first.
		zero_status = dig_zero_regions()

		if zero_status == -1:
			running = False
			break
	
		constraint_cells, constraint_mines, scan_status = build_constraints_incremental()
	
		if scan_status != 1:
	
			running = False
			break
	
		# --------------------------------------
		# 2. Close deterministic constraints.
		# --------------------------------------
	
		constraint_cells, constraint_mines, safe_cells, mine_cells, deduction_status = close_constraints_parallel(
			constraint_cells,
			constraint_mines
		)
	
		if deduction_status != 1:
	
			running = False
			break
	
		# --------------------------------------
		# 3. Apply deductions centrally.
		# --------------------------------------
	
		changed = False
	
		for i in range(len(mine_cells)):
	
			cell = mine_cells[i]
	
			if state[cell] == UNKNOWN:
	
				state[cell] = MINE
				mark_cell_changed(cell)
				changed = True
	
		for i in range(len(safe_cells)):
	
			cell = safe_cells[i]
	
			if state[cell] == UNKNOWN:
	
				state[cell] = SAFE
				mark_cell_changed(cell)
				changed = True

		# --------------------------------------
		# 4. Dig all known-safe tiles in parallel.
		# --------------------------------------
	
		# Expand all available zero regions first.
		zero_status = dig_zero_regions()

		if zero_status == -1:
			running = False
			break

		# Dig any remaining known-safe cells.
		dug = dig_safe_cells_parallel()

		if dug == -1:
			running = False
			break

		if dug > 0:
			continue

		# --------------------------------------
		# 5. No guaranteed-safe tiles.
		#    Calculate probabilities.
		# --------------------------------------
	
		frontier, frequencies, solution_counts, probability_status = calculate_component_probabilities(
			constraint_cells,
			constraint_mines
		)
	
		if probability_status != 1:
	
			running = False
			break
	
		best = -1
	
		for i in range(len(frontier)):
	
			if solution_counts[i] > 0:
	
				if best == -1:
	
					best = i
	
				else:
	
					left = frequencies[i] * solution_counts[best]
					right = frequencies[best] * solution_counts[i]
	
					if left < right:
						best = i
	
		if best == -1:
	
			running = False
			break

		# --------------------------------------
		# 6. Make one probabilistic guess.
		# --------------------------------------
	
		target = frontier[best]

		move_to_cell(target)
		dig()

		state[target] = SOOT
		numbers[target] = measure()
		register_zero(target)

		mark_cell_changed(target)

		if numbers[target] == None:
			running = False
			break

	# ==========================================
	# SOLVER FINISHED
	# ==========================================
			
if __name__ == "__main__":
	clear()
	jump(Unlocks.Dynamite)
	while True:
		#while get_pos_z() > -600:
		#	dig()
		#while get_ground_type() != Grounds.Dynamite:
		#	dig()
		dynamite_full()
		while get_ground_type() != Grounds.Dynamite:
			dig()