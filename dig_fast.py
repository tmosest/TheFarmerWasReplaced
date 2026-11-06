# Using the bug from rice we are able to dig really fast down
from rice import dig_parallel_to_clay

if __name__ == "__main__":
	clear()
	# jump(Unlocks.Rice)
	dig_parallel_to_clay()
	# generate_rice_parallel()
	
	while True:
		print("z pos ", get_pos_z())
		dig_parallel_to_clay()
		print("z pos ", get_pos_z())
		for _ in range(5):
			dig()