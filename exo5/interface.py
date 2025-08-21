import pygame # recuperer les composants
import numpy 
pygame.init()

# creer une classe qui va gérer la notion d'emplacement
class Emplacement(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('assets/pomme_dore.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def set_image(self, image):
        self.image = image                        

# definir une fonction lancement
def lancement():
                              
    global jetons

    # choix au hasard selon les probabilités
    hasard = numpy.random.choice(fruits, 3, p=proba_fruits)
    fruit_gauche = fruits_dict[hasard[0]]
    fruit_milieu = fruits_dict[hasard[1]]
    fruit_droite = fruits_dict[hasard[2]]

    # changement des images
    emplacement_gauche.set_image(fruit_gauche)   
    emplacement_milieu.set_image(fruit_milieu)
    emplacement_droite.set_image(fruit_droite)

    # faire la verification des lots
    if hasard[0] == hasard[1] == hasard[2]: # les 3 premiers fruits sont identique
        fruit = hasard[0]
        jetons_gagnes = fruits_dict_gains[fruit]
        jetons += jetons_gagnes 
        print(f"Une ligne de {fruit} a été completé ! + {jetons_gagnes} Jetons")
  
# creation de la fenetre
largeur = 800
hauteur = 460                                  
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Machine à sous - GravenFruitiiiii")
blanc = [255, 255, 255] # couleur blanche

# argent du joueur
jetons = 1000

# dictionnaire de fruits
image_test = pygame.image.load('assets/orange.png')
fruits_dict = {
    "cerise": pygame.image.load('assets/cerise.png'),
    "ananas": pygame.image.load('assets/ananas.png'),
    "orange": pygame.image.load('assets/orange.png'),
    "pasteque": pygame.image.load('assets/pasteque.png'),
    "pomme_dore": pygame.image.load('assets/pomme_dore.png')
}

# liste stockant le nom de chaque fruit
fruits = ["ananas", "cerise", "orange", "pasteque", "pomme_dore"]
proba_fruits = [0.2, 0.25, 0.4, 0.1, 0.05]

fruits_dict_gains = {
    "orange": 5,
    "cerise": 15,
    "ananas": 50,
    "pasteque": 150,
    "pomme_dore": 10000
}

# chargement des emplacements
hauteur_emplacement = hauteur / 2 + 30 
emplacement_x_milieu = largeur / 3 + 62    
emplacement_x_gauche = emplacement_x_milieu - image_test.get_width() - 22
emplacement_x_droite = emplacement_x_milieu + image_test.get_width() + 20

emplacements = pygame.sprite.Group()
emplacement_gauche = Emplacement(emplacement_x_gauche, hauteur_emplacement)
emplacement_milieu = Emplacement(emplacement_x_milieu, hauteur_emplacement)
emplacement_droite = Emplacement(emplacement_x_droite, hauteur_emplacement)

# rangement des emplacements dans le groupe
emplacements.add(emplacement_gauche)
emplacements.add(emplacement_milieu)
emplacements.add(emplacement_droite)

# charger l'image de l'arriere plan
fond = pygame.image.load('assets/slot.png') 
police = pygame.font.SysFont("comicsansms", 30)

# boucle pour maintenir la fenetre pygame en eveil
running = True

while running:

    ecran.fill(blanc)
    ecran.blit(fond, (0, 0))
    emplacements.draw(ecran)

    # afficher son nombre de jetons
    text = police.render(str(jetons) + " jetons", True, (0, 0, 0))
    ecran.blit(text, (10, 0))
    
    pygame.display.flip()    

    for event in pygame.event.get():
        # verifier si le joueur ferme la fenetre
        if event.type == pygame.QUIT:
            running = False
            quit()
        # verifier si le joueur appuie sur une touche
        if event.type == pygame.KEYDOWN:
            # si la touche est la touche ESPACE
            if event.key == pygame.K_SPACE and jetons >= 10:
                lancement() # appeler la fonction
                jetons -= 10