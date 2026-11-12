from reset_util import *
from reset_multi import *
from reset_need import *
from reset_farm import *
from reset_dino import *
from reset_maze import *

def pt10000():
	tree_avto_start(40500)
	hay_avto_start(40500)
	carrot_avto_start(20000)
	pumpkin_avto_start(10000)

def pt20000(num):
	clear()
	tree_avto_start(num*40)
	hay_avto_start(num*40)
	carrot_avto_start(num*5)
	pumpkin_avto_start(num)
	tree_avto_start(num*10)
	hay_avto_start(num*10)

need()

hay_avto_start(500)
unlock(Unlocks.Plant)
unlock(Unlocks.Expand)

bush_avto_start(1000)
unlock(Unlocks.Carrots)
unlock(Unlocks.Expand)

bush_avto_start(1000)
carrot_avto_start(300)
unlock(Unlocks.Trees)
unlock(Unlocks.Expand)

tree_avto_start(500)
carrot_avto_start(200)
unlock(Unlocks.Pumpkins)

tree_avto_start(10500)
hay_avto_start(10500)
carrot_avto_start(7500)
pumpkin_avto_start(5000)
unlock(Unlocks.Watering)
unlock(Unlocks.Fertilizer)
unlock(Unlocks.Cactus)

tree_avto_start(10500)
hay_avto_start(10500)
carrot_avto_start(7500)
pumpkin_avto_start(7500)
unlock(Unlocks.Expand)
unlock(Unlocks.Expand)
unlock(Unlocks.Expand)
unlock(Unlocks.Expand)

tree_avto_start(10500)
hay_avto_start(10500)
carrot_avto_start(7500)
pumpkin_avto_start(7500)

unlock(Unlocks.Cactus)

cactus_avto_start(5000)
if unlock(Unlocks.Dinosaurs):
	quick_print('dino ok')
	
unlock(Unlocks.Speed)
quick_print(num_unlocked(Unlocks.Speed))
unlock(Unlocks.Speed)
quick_print(num_unlocked(Unlocks.Speed))
unlock(Unlocks.Speed)
quick_print(num_unlocked(Unlocks.Speed))
unlock(Unlocks.Speed)
quick_print(num_unlocked(Unlocks.Speed))
unlock(Unlocks.Speed)
quick_print(num_unlocked(Unlocks.Speed))

pt10000()
unlock(Unlocks.Grass)
unlock(Unlocks.Grass)
unlock(Unlocks.Grass)
unlock(Unlocks.Trees)
unlock(Unlocks.Trees)
unlock(Unlocks.Trees)
unlock(Unlocks.Carrots)
unlock(Unlocks.Carrots)
unlock(Unlocks.Carrots)
unlock(Unlocks.Pumpkins)
unlock(Unlocks.Pumpkins)
unlock(Unlocks.Pumpkins)
quick_print(num_unlocked(Unlocks.Carrots))
quick_print(num_unlocked(Unlocks.Pumpkins))

pt10000()

quick_print(get_cost(Entities.Carrot))
quick_print(get_cost(Entities.Pumpkin))
quick_print(get_cost(Entities.Cactus))
quick_print(get_cost(Entities.Apple))


pt20000(10000)
Weird_avto_start(10000)
if unlock(Unlocks.Mazes):
	quick_print('maze ok')
quick_print(num_items(Items.Weird_Substance))
quick_print(get_world_size())
substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
quick_print(substance)

while num_items(Items.Gold) < 1000000:
	if num_items(Items.Weird_Substance) < 1200:
		tree_avto_start(40000)
		hay_avto_start(40000)
		Weird_avto_start(1500)
	else:
		clear()
		harvest()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)
		complete_maze()

quick_print(num_items(Items.Gold))

while num_items(Items.Bone) < 2000000:
	if num_items(Items.Cactus) < 1000:
		pt20000(10000)
		cactus_avto_start(10000)
	clear()
	farm_bone()

quick_print(num_items(Items.Bone))

if unlock(Unlocks.Leaderboard):
	quick_print("yay")