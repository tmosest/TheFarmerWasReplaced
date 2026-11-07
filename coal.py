from dig_util import dig_tracking_parallel

def dig_coal_parallel():
	dont_dig_set = {Grounds.Rock, Grounds.Mushroom, Grounds.Basalt, Grounds.Dynamite, Grounds.Clay, Grounds.Iron, Grounds.Sand}
	
	while True:
		found_dont_dig = False
		while found_dont_dig == False:
			map = dig_tracking_parallel(dont_dig_set)
			for ground in dont_dig_set:
				if ground in map:
					found_dont_dig = True
					
		clear()
	

if __name__ == "__main__":
	clear()
	dig_coal_parallel()	