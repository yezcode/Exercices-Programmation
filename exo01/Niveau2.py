import random

keys = 0
snake_jar = random.randint(1, 5)

while keys != 3:
    choice = int(input("Choisit une jarre : 1, 2, 3, 4, 5"))
    if choice == snake_jar:
        keys -= 1
        print("Perdu ! vous tombez dans le piège (", keys, "/3) !")
    else:
        keys += 1
        print("Gagné ! vous avez obtenu une clé (", keys, "/3) !")

print("Tu deviens roi du temple")