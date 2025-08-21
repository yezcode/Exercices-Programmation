import random # pour faire des choses au hasard
import pygame # recuperer les composants


# créer une classe qui va representer l'oeuf en chocolat
class OeufChocolat(pygame.sprite.Sprite):

    # definir la fonction init qui charge les caracteristiques de base de notre oeuf
    def __init__(self, largeur_ecran, hauteur_ecran, panier):
        super().__init__()
        self.vitesse_chute = random.randint(1, 3)
        self.panier = panier
        self.panier_group = pygame.sprite.Group()
        self.panier_group.add(self.panier)
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.image = pygame.image.load('assets/oeuf.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, largeur_ecran - 40)

    # teleporter respawn
    def repositionner(self):
        # reteleporter l'oeuf en haut
        self.rect.x = random.randint(20, self.largeur_ecran - 40)
        self.rect.y = - self.image.get_height()
        self.vitesse_chute = random.randint(1, 3)

    # une methode pour deplacer vers le bas l'oeuf, chuter
    def gravite(self):
        self.rect.y += self.vitesse_chute

        # si il touche le panier
        if pygame.sprite.spritecollide(self, self.panier_group, False, pygame.sprite.collide_mask) and self.rect.y >= 360:
            print("Collision", self.rect.y)
            self.repositionner()
            # ajouter des points
            self.panier.ajouter_points()


        # si il sort de l'ecran
        if self.rect.y >= self.hauteur_ecran:
            self.repositionner()
            # enlever les points
            self.panier.enlever_points()