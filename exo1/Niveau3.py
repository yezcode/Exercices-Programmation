import random

print("Bienvenue dans le jeu !")

# choix du parametrage/niveau de difficulté
level = int(input("Ecrit 1:facile, 2:moyen, 3:difficile"))

# compteur de clés magique
trousseaux = 0

# repeter les manches de notre jeu
while trousseaux != 3:
    print("Vous disposez de 5 jarres devant vous. Choisit 1, 2, 3, 4 ou 5")

    # on genere autant de serpent que le niveau
    snakes = ['S'] * level

    # on genere autant de jarres non infectés que la difference
    keys = ['K'] * (5 - level)

    # on combine les jarres inféctés avec les non inféctés
    jars = snakes + keys

    # on melange les jarres infectés avec les clés magique
    random.shuffle(jars)

    # demande à notre joueur de mettre une valeur
    choix = int(input())

    print("Le joueur a mit la jarre n°", choix)

    # verification
    if jars[choix-1] == 'K': #gagné
        print("Gagné ! tu obtiens une clé magique ! La jarre infécté était", jars)
        trousseaux += 1
        print("Tu as actuellement", trousseaux, "/3 clés")
    else:
        print("Perdu ! un serpent apparait !")
        
        # si le joueur n'a pas de clé
        if trousseaux > 0:
            trousseaux -= 1
            print("Tu as actuellement", trousseaux, "/3 clés")
            print(f"Tu as actuellement {trousseaux}/3 clés")
            print("Tu as actuellement" + str(trousseaux) + "/3 clés")

print("Tu deviens le roi du temple !")