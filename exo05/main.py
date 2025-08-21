import random
import numpy
#Niveau 1
# liste stockant le nom de chaque fruit
#fruits = ["ananas", "cerise", "orange", "pasteque", "pomme_dore"]

# choix au hasard 
#hasard = random.choices(fruits, k=3)

#print(hasard)

# liste stockant le nom de chaque fruit
fruits = ["ananas", "cerise", "orange", "pasteque", "pomme_dore"]
proba_fruits = [0.2, 0.25, 0.4, 0.1, 0.05]

fruits_dict = {
    "orange": 5,
    "cerise": 15,
    "ananas": 50,
    "pasteque": 150,
    "pomme_dore": 10000
}

# choix au hasard selon les probabilités
hasard = numpy.random.choice(fruits, 3, p=proba_fruits)

# afficher le tirage
print(hasard)

# faire la verification des lots
if hasard[0] == hasard[1] == hasard[2]: # les 3 premiers fruits sont identique
    fruit = hasard[0]
    jetons = fruits_dict[fruit]
    print(f"Une ligne de {fruit} a été completé ! + {jetons} Jetons")