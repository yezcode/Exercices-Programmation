import random

snake_jar = random.randint(1, 5)
choice = int(input("Choisit une jarre : 1, 2, 3, 4, 5"))

if choice == snake_jar:
    print("Perdu ! vous tombez dans le piège !")
else:
    print("Gagné ! vous avez obtenu une clé !")
    