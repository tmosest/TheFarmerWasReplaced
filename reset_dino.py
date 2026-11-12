def calculate_pair_steps(world_size):
	return (world_size - 6) // 2 + 2
def try_move(direction):
	return move(direction)
def go_to_origin():
	while get_pos_x() != 0:
		try_move(West)
	# Move vertically toward Y=0
	while get_pos_y() != 0:
		try_move(South)
def return_and_reset():
	change_hat(Hats.Straw_Hat)
	go_to_origin()
	change_hat(Hats.Dinosaur_Hat)
	perform_dino_pattern()
def repeat_move(direction, steps):
	for _ in range(steps):
		if not try_move(direction):
			# If a move fails, reset and indicate failure to the caller
			return_and_reset()
			return False
	return True
def perform_dino_pattern():
	world_size = get_world_size()
	max_index = world_size - 1
	pair_steps = calculate_pair_steps(world_size)
	while num_items(Items.Cactus) > 1000:
		# Climb to the top edge (Y = max_index)
		if not repeat_move(North, max_index):
			return
		# Run to the right edge (X = max_index)
		if not repeat_move(East, max_index):
			return
		# Drop one row to start the sweep pairs
		if not repeat_move(South, 1):
			return
		# Perform pair_steps times: sweep left, step down, sweep right, step down
		for _ in range(pair_steps):
			# Sweep left across most of the row
			if not repeat_move(West, max_index - 1):
				return
			# Move down a single row
			if not repeat_move(South, 1):
				return
			# Sweep right across most of the next row
			if not repeat_move(East, max_index - 1):
				return
			# Move down a single row to continue the pattern
			if not repeat_move(South, 1):
				return
		# After the pairs, move back to the leftmost edge to finish the loop
		if not repeat_move(West, max_index):
			return
def farm_bone():
	world_size = get_world_size()
	# If the world size is odd, reduce it by 1 to make it even
	if world_size % 2 == 1:
		set_world_size(world_size - 1)
		world_size -= 1
	# Visual preparation and positioning
	change_hat(Hats.Straw_Hat)
	go_to_origin()
	change_hat(Hats.Dinosaur_Hat)
	# Run the pattern repeatedly until the environment prevents movement
	while num_items(Items.Cactus) > 1000:
		perform_dino_pattern()

 