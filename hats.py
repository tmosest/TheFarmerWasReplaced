def random_hats():
	hats = [Hats.Brown_Hat, Hats.Cactus_Hat, Hats.Carrot_Hat, Hats.Gold_Hat, Hats.Gray_Hat, Hats.Gray_Hat, Hats.Green_Hat, Hats.Pumpkin_Hat, Hats.Pumpkin_Hat, Hats.Purple_Hat, Hats.Traffic_Cone, Hats.Tree_Hat, Hats.Wizard_Hat]
	index = random() * len(hats)
	change_hat(hats[index])