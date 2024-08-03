import pygame
import random
from classe import Missile
import sys


def attendre_commencer(fenetre, largeur_fenetre, hauteur_fenetre, son, manette=None):
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    police = pygame.font.Font(None, 74)
    texte = police.render("Appuyez sur A pour commencer", True, blanc)
    rect_texte = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    
    attendre = True

    while attendre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestion de la manette
        if manette:
            manette.init()  # Assure que la manette est initialisée
            boutons = [manette.get_button(i) for i in range(manette.get_numbuttons())]
            if boutons[0]:  # Bouton A
                son.play()
                attendre = False
            elif attendre == True:
                fenetre.fill(noir)
                fenetre.blit(texte, rect_texte)
                pygame.display.flip()

        pygame.time.delay(100)  # Petite pause pour éviter l'utilisation excessive du CPU
        

def afficher_score(fenetre, score):
    blanc = (255, 255, 255)
    police = pygame.font.Font(None, 36)
    texte = police.render(f'Score: {score}', True, blanc)
    fenetre.blit(texte, (10, 50))


def afficher_game_over(fenetre, largeur_fenetre, hauteur_fenetre, point):
    # Définir les couleurs
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    # Définir la police
    police = pygame.font.Font(None, 74)
    police2 = pygame.font.Font(None, 25)

    # Créer le message de game over
    texte = police.render("GAME OVER", True, blanc)
    texte_2 = police2.render(f"Score final: {point} points", True, blanc)
    texte_rect = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    texte_rect2 = texte_2.get_rect(center=(largeur_fenetre //2 , hauteur_fenetre - 200))

    # Remplir l'écran de noir
    fenetre.fill(noir)
    
    # Dessiner le message de game over
    fenetre.blit(texte, texte_rect)
    fenetre.blit(texte_2, texte_rect2)
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    
    # Attendre que l'utilisateur appuie sur une touche ou ferme la fenêtre
    attendre_quitter()


def attendre_quitter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()


def generer_missile(largeur_fenetre, niveau):
    """
    Génère un missile ennemi à une position aléatoire en haut de l'écran.

    Args:
        largeur_fenetre (int): Largeur de la fenêtre de jeu.
    
    Returns:
        Missile: Un nouvel objet Missile.
    """
    x = random.randint(0, largeur_fenetre)
    y = 0
    vitesse_x = 0
    vitesse_y = 0.5  # Ajuster la vitesse 
    return Missile(x, y, vitesse_x, vitesse_y, niveau)

def gagner(fenetre, point, largeur_fenetre, hauteur_fenetre):

    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    # Définir la police
    police = pygame.font.Font(None, 74)
    police2 = pygame.font.Font(None, 25)

    # Créer le message de game over
    texte = police.render("Vous gagnez!", True, blanc)
    texte2 = police2.render(f"Vous avez un score de {point} points", True, blanc)
    texte_rect = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    texte_rect2 = texte2.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre - 200))
    
    # Remplir l'écran de noir
    fenetre.fill(noir)
    
    # Dessiner le message de game over
    fenetre.blit(texte, texte_rect)
    fenetre.blit(texte2, texte_rect2)
    # Mettre à jour l'affichage
    pygame.display.flip()
    
    # Attendre que l'utilisateur appuie sur une touche ou ferme la fenêtre
    attendre_quitter()