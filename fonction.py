import pygame
import random
from classe import Missile

def fin_de_partie(texte, police, taille, couleur):
    font = pygame.font.Font(police, taille)
    surface_texte = font.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect()
    return surface_texte, rect_texte

def generer_missile(largeur_fenetre):
    x = random.randint(0, largeur_fenetre - 10)  # Assurer que le missile reste dans les limites de la fenêtre
    y = 0
    vitesse_x = random.uniform(-0.1, 0.1)
    vitesse_y = random.uniform(0.1, 0.4)
    return Missile(x, y, vitesse_x, vitesse_y)

