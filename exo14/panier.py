import pygame # importe les composants


# créer une classe qui va representer le concept de joueur ou du panier sur notre jeu
class Panier(pygame.sprite.Sprite):

    # le constructeur
    def __init__(self, largeur_ecran, hauteur_ecran):
        super().__init__()
        self.largeur_ecran = largeur_ecran
        self.points = 50 # nombre de points qu'aura le joueur
        self.maximum_points = 100 # nombre maximum de points
        self.image = pygame.image.load('assets/panier.png') # charger l'image du panier
        self.image = pygame.transform.scale(self.image, (120, 120)) # redimentionner l'image
        self.rect = self.image.get_rect() # on lui definit un rectangle
        self.rect.x = (largeur_ecran / 2) - self.image.get_width() /2
        self.rect.y = hauteur_ecran - 180
        self.vitesse = 6 # vitesse de deplacement du panier

    # methode pour ajouter 5 points
    def ajouter_points(self):
        if self.points + 5 <= self.maximum_points: # limite de points
            print("+5 points")
            self.points += 5

    # methode enlever 2 points
    def enlever_points(self):
        if self.points - 2 > 0: 
            print("-2 points")
            self.points -= 2
        else:
            # perdu
            print("Perdu")

    # methode pour le deplacement droite
    def deplacement_droite(self):
        if self.rect.x + self.image.get_width() < self.largeur_ecran: 
            self.rect.x += self.vitesse

    # methode pour le deplacement gauche
    def deplacement_gauche(self):
        if self.rect.x > 0:
            self.rect.x -= self.vitesse