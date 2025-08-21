import pygame

pygame.init()
largeur = 800
hauteur = 460
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Machine à sous - GravenFruitiiiii")
blanc = [255, 255, 255] 
running = True

while running:

    ecran.fill(blanc)
    pygame.display.flip()
    for event in pygame.event.get():
    # verifier si le joueur ferme la fenetre
        if event.type == pygame.QUIT:
            running = False
            quit()
            