from panier import Panier # on importe le composant panier
from oeuf import OeufChocolat # on import la classe oeuf chocolat
import pygame # utiliser le module pygame pour faire des jeux avec python
pygame.init() # charger les composants

# definir les dimentions
largeur = 800
hauteur = 480

# creer la fenetre avec pygame
fenetre = pygame.display.set_mode((largeur, hauteur)) # on definit la taille
pygame.display.set_caption("Chasse aux oeufs") # on definit un titre
pygame.display.set_icon(pygame.image.load('assets/panier.png'))

# maintenir la fenetre du jeu en eveil pour pas qu'elle se ferme
running = True

fond = pygame.image.load('assets/fond.jpg') # charger l'image de l'arrière plan
sol = pygame.image.load('assets/sol.png') # charger l'image du sol

# charger la barre de chocolat
bar_chocolat = pygame.image.load('assets/chocolate.png') 

# redimentionner
bar_chocolat = pygame.transform.scale(bar_chocolat, (60, 60))

# créer un dictionnaire qui va contenir en temps reel les touches enclenchées par le joueur
touches_active = {}

# créer le panier du joueur
panier = Panier(largeur, hauteur)

# créer la couleur
chocolat_couleur = (87, 64, 53)

# créer un groupe qui va contenir plusieurs oeufs en chocolat
oeufs = pygame.sprite.Group()
oeufs.add(OeufChocolat(largeur, hauteur, panier))
oeufs.add(OeufChocolat(largeur, hauteur, panier))

# tant que la fenetre est active, on boucle des instructions à chaque fois
while running:

    # actualiser toutes les images qui sont sur le jeu
    fenetre.blit(fond, (0, 0))
    oeufs.draw(fenetre)
    fenetre.blit(panier.image, panier.rect)
    fenetre.blit(sol, (0, 0))

    largeur_chocolat = panier.points * 3 - 20

    # dessiner l'arriere de la jauge
    pygame.draw.rect(fenetre, (128, 128, 128), [10, hauteur - 50, largeur - 20, 32] )
    pygame.draw.rect(fenetre, chocolat_couleur, [10, hauteur - 50, largeur_chocolat, 32] )

    # on place la bar de chocolat
    fenetre.blit(bar_chocolat, (largeur_chocolat - bar_chocolat.get_width() / 2, 420))

    # recupere tout les oeufs depuis mon groupe de sprite
    for oeuf in oeufs:
        oeuf.gravite()

    # detecter quelle est la touche active par le joueur
    if touches_active.get(pygame.K_RIGHT): # si la touche droite est active
        panier.deplacement_droite()
    elif touches_active.get(pygame.K_LEFT): # si la touche gauche est active
        panier.deplacement_gauche()

    # mettre à jour l'ecran du jeu
    pygame.display.flip()

    # boucler sur les evenements actif du joueur
    for evenement in pygame.event.get():
        # si l'evenement c'est la fermeture de fenetre
        if evenement.type == pygame.QUIT:
            running = False # on arrete la boucle pour que la fenetre se ferme
            quit() # on quitte le jeu
        # si l'evenement est une interaction au clavier
        elif evenement.type == pygame.KEYDOWN:
            touches_active[evenement.key] = True # la touche est active
        elif evenement.type == pygame.KEYUP:
            touches_active[evenement.key] = False # la touche est desactive