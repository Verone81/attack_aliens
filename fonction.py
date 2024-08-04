import pygame
import random
from classe import Missile
import sys


def attendre_commencer(fenetre, largeur_fenetre, hauteur_fenetre, son, manette=None):
    """
    Affiche un message d'attente et commence le jeu lorsque le bouton A de la manette est pressé.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre de jeu.
        largeur_fenetre (int): La largeur de la fenêtre de jeu.
        hauteur_fenetre (int): La hauteur de la fenêtre de jeu.
        son (pygame.mixer.Sound): Le son à jouer lorsqu'on appuie sur le bouton A.
        manette (pygame.joystick.Joystick, optional): La manette à utiliser pour démarrer le jeu. Default à None.
    """
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

        if attendre:
            fenetre.fill(noir)
            fenetre.blit(texte, rect_texte)
            pygame.display.flip()

        pygame.time.delay(100)  # Petite pause pour éviter l'utilisation excessive du CPU


def afficher_score(fenetre, score):
    """
    Affiche le score actuel dans le coin supérieur gauche de l'écran.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre de jeu.
        score (int): Le score actuel du joueur.
    """
    blanc = (255, 255, 255)
    police = pygame.font.Font(None, 36)
    texte = police.render(f'Score: {score}', True, blanc)
    fenetre.blit(texte, (10, 50))


def afficher_game_over(fenetre, largeur_fenetre, hauteur_fenetre, point):
    """
    Affiche l'écran de game over avec le score final.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre de jeu.
        largeur_fenetre (int): La largeur de la fenêtre de jeu.
        hauteur_fenetre (int): La hauteur de la fenêtre de jeu.
        point (int): Le score final du joueur.
    """
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    police = pygame.font.Font(None, 74)
    police2 = pygame.font.Font(None, 25)

    texte = police.render("GAME OVER", True, blanc)
    texte_2 = police2.render(f"Score final: {point} points", True, blanc)
    texte_rect = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    texte_rect2 = texte_2.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre - 200))

    fenetre.fill(noir)
    
    fenetre.blit(texte, texte_rect)
    fenetre.blit(texte_2, texte_rect2)
    
    pygame.display.flip()
    
    attendre_quitter()


def attendre_quitter():
    """
    Attend que l'utilisateur appuie sur une touche ou ferme la fenêtre pour quitter le jeu.
    """
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
        largeur_fenetre (int): La largeur de la fenêtre de jeu.
        niveau (int): Le niveau du missile.

    Returns:
        Missile: Un nouvel objet Missile.
    """
    x = random.randint(0, largeur_fenetre)
    y = 0
    vitesse_x = 0
    vitesse_y = 0.5  # Ajuster la vitesse 
    return Missile(x, y, vitesse_x, vitesse_y, niveau)


def gagner(fenetre, point, largeur_fenetre, hauteur_fenetre):
    """
    Affiche l'écran de victoire avec le score final.

    Args:
        fenetre (pygame.Surface): La surface de la fenêtre de jeu.
        point (int): Le score final du joueur.
        largeur_fenetre (int): La largeur de la fenêtre de jeu.
        hauteur_fenetre (int): La hauteur de la fenêtre de jeu.
    """
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    police = pygame.font.Font(None, 74)
    police2 = pygame.font.Font(None, 25)

    texte = police.render("Vous gagnez!", True, blanc)
    texte2 = police2.render(f"Vous avez un score de {point} points", True, blanc)
    texte_rect = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    texte_rect2 = texte2.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre - 200))
    
    fenetre.fill(noir)
    
    fenetre.blit(texte, texte_rect)
    fenetre.blit(texte2, texte_rect2)
    
    pygame.display.flip()
    
    attendre_quitter()
