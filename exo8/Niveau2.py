import random, string

# créer une fonction qui va se charger de générer cette chaine (code secret)
def generer_code_debloquage():
    # Format du code de déblocage : AAAA-2222-XX 
    lettres = string.ascii_uppercase

    mot = ''.join(random.choice(lettres) for i in range(4))
    numeros = random.randint(1000, 9999)
    chars = ''.join(random.choice(lettres) for i in range(2))

    # choisir une lettre
    code = mot + "-" + str(numeros) + '-' + chars
    print("Votre code débloquage est: ", code)
    return code

# créer une fonction afficher_parking pour afficher le status de chaque emplacement
def afficher_parking():
    # boucle parcourir chaque emplacement pour afficher la disponibilité
    for num_etage, etage in enumerate(parking, start=1):
        for num_place, place in enumerate(etage, start=1):
            # nom_variable = (condition_faux, condition_vrai)[condition à verifier]
            resultat = ("Non Disponible", "Disponible")[place == 'D']
            resultat = (resultat, "Réservée")[place == 'H']

            print("Etage n° -", num_etage, " place n°", num_place, resultat)

# afficher un message de bienvenue
print("Bienvenue au niveau -1, que souhaitez-vous faire ?")



# creation de la liste
emplacements = 27
etages = 3
parking = [['D'] * emplacements] * etages

# créer une liste qui contient un dico par etage avec les codes à débloquer
code_debloquage = [
    {},
    {},
    {}
]

afficher_parking()

# je creer une boucle qui ne va jamais s'arreter
while True:
    
    # appeler la fonction pour afficher le parking
    # afficher_parking()

    print("Choisissez un numero d'étage")

    # proposer à notre client de choisir un étage
    choix_etage = int(input()) - 1

    if choix_etage >= 0 and choix_etage < len(parking):
        print("Vous avez choisi l'etage n°", choix_etage + 1)

        # proposer à notre client de faire une action
        print("1: Garer une voiture, 2: Récuperer une voiture")
        choix = int(input())

        # verifier le choix
        if choix == 1:
            print("Vous avez choisi de garer une voiture, à quel emplacement souhaitez vous la mettre ?")
            choix_emplacement = int(input()) - 1

            # verifier si la place est disponible
            if len(parking[choix_etage]) > choix_emplacement >= 0:
                if parking[choix_etage][choix_emplacement] == 'D': # si c'est dispo
                    print("Vous avez prit la place n°", choix_emplacement + 1)
                    parking[choix_etage][choix_emplacement] = 'V'
                    # génerer le code secret
                    code_secret = generer_code_debloquage()
                    code_debloquage[choix_etage][choix_emplacement] = code_secret

                else:
                    print("Emplacement non disponible")

        elif choix == 2:
            print("Récuperer une voiture, mettre le numero de place: ")

            choix_emplacement = int(input()) - 1

            # verifier si la place existe
            if len(parking[choix_etage]) > choix_emplacement >= 0:
                if parking[choix_etage][choix_emplacement] == 'V':

                    print("Entrer le code secret")

                    # demander le code secret de la voiture
                    choix_code_secret = input()

                    # verifier si le code secret est bon
                    code_secret_atrouver = code_debloquage[choix_etage][choix_emplacement]

                    # comparer
                    if choix_code_secret == code_secret_atrouver:
                        print("Vehicule récupéré")
                        parking[choix_etage][choix_emplacement] = 'D'
                        print("L'emplacement n°", choix_emplacement + 1, "est désormais disponible")
                    else:
                        print("Code incorrecte ! stop !")

        else:
            print("Erreur, vous devez ecrire 1 ou 2")

        # afficher le parking
        # afficher_parking()

    else:
        print("Etage non existant !")