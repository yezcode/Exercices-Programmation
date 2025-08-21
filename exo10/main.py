import math # differents calculs mathematiques
import time # gerer le temps

# créer une classe qui va gerer la notion de lave linge
class LaveLinge:

    # creer le constructeur
    def __init__(self, tours_minutes=1400, contenance_kg=8):
        self.tours_minutes = tours_minutes
        self.contenance_kg = contenance_kg
        self.contenance_actuel_kg = 0
        self.temperature_actuel = 60
        self.duree_machine_defaut = 35
        self.duree_machine = 35
        print("Nouvelle machine ajoutée à la laverie")
        print("tours min: ", self.tours_minutes, "contenance:", contenance_kg)


    # methodes
    def inserer_linge(self, poids_kg):
        print("Vous ouvrez la machine et vous entrez un total de", poids_kg, "kg")

        # verification
        if poids_kg <= self.contenance_kg:
            print("Ok ! le linge est à l'interieur")
            self.contenance_actuel_kg = poids_kg
        else:
            print("Ah non ! la machine est trop petite")

    def demarrage(self):

        # verifier si la machine est vide
        if self.contenance_actuel_kg != 0:
            # creer une variable pour stocker le temps par défaut de la machine
            compteur_tours = 0

            # une boucle tant que la machine n'est pas à 0
            while self.duree_machine > 0:
                print(str(self.duree_machine) + "s")
                self.duree_machine -= 1
                compteur_tours += 1400
                time.sleep(1) # attendre 1s

            # afficher nombre de tours minutes
            print("Fin", compteur_tours, "tours minutes")
        else:
            print("Vous n'avez pas inserer de linge !")

    def stop(self):
        if self.duree_machine > 0:
            print("Arret ok !")
            self.duree_machine = 0
        else:
            print("Arret impossible, lave linge en cours d'utilisation")



# afficher un message dans la console
print("Ouverture de la machine à laver")

# appeler la fonction pour demarrer la machine à laver
machine = LaveLinge(1200, 12)

# dictionnaire avec nos vetements et leurs poids
vetements = {
    "chemise rouge bleuté": 1,
    "manteau de gravounai": 6,
    "chaussettes": 4,
    "jean de yannis": 18
}

total_kg = 0.0

for poid in vetements.values():
    total_kg += poid

print("Vous avez", total_kg, "kg de vetements")

# calculer combien de machines
machines = math.ceil(total_kg / 8)
print(machines, "machines")

# calculer la consommation d'eau
consommation_eau = machines * 60
print("La consommation d'eau pour {} machines est de {}L".format(machines, consommation_eau))

# appeler la methode inserer linge
machine.inserer_linge(total_kg)

# appeler la methode demarrer la machine
machine.demarrage()
machine.stop()