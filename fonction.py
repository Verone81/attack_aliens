import pygame
import random
from classe import Missile
import sys


def afficher_ecran_depart(fenetre, largeur_fenetre, hauteur_fenetre):
    # Définir les couleurs
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    # Définir la police
    police_titre = pygame.font.Font(None, 74)
    police_instructions = pygame.font.Font(None, 36)
    
    # Créer le message de titre
    texte_titre = police_titre.render("Attack d'Aliens", True, blanc)
    texte_titre_rect = texte_titre.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 - 50))
    
    # Créer le message d'instructions
    texte_instructions = police_instructions.render("Appuyez sur une touche pour commencer", True, blanc)
    texte_instructions_rect = texte_instructions.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 + 50))
    
    # Remplir l'écran de noir
    fenetre.fill(noir)
    
    # Dessiner le message de titre et d'instructions
    fenetre.blit(texte_titre, texte_titre_rect)
    fenetre.blit(texte_instructions, texte_instructions_rect)
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    
    # Attendre que l'utilisateur appuie sur une touche ou ferme la fenêtre
    attendre_commencer()


def attendre_commencer(fenetre, largeur_fenetre, hauteur_fenetre, manette=None):
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    police = pygame.font.Font(None, 74)
    texte = police.render("Appuyez sur A pour commencer", True, blanc)
    rect_texte = texte.get_rect(center=(largeur_fenetre / 2, hauteur_fenetre / 2))

    attendre = True
    while attendre:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        fenetre.fill(noir)
        fenetre.blit(texte, rect_texte)
        pygame.display.flip()

        if manette:
            boutons = [manette.get_button(i) for i in range(manette.get_numbuttons())]
            if boutons[0]:  # Bouton A
                attendre = False
        else:
            touches = pygame.key.get_pressed()
            if touches[pygame.K_RETURN]:  # Touche Entrée pour tester sans manette
                attendre = False


def afficher_score(fenetre, score):
    blanc = (255, 255, 255)
    police = pygame.font.Font(None, 36)
    texte = police.render(f'Score: {score}', True, blanc)
    fenetre.blit(texte, (10, 50))


def afficher_game_over(fenetre, largeur_fenetre, hauteur_fenetre):
    # Définir les couleurs
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    
    # Définir la police
    police = pygame.font.Font(None, 74)
    
    # Créer le message de game over
    texte = police.render("GAME OVER", True, blanc)
    texte_rect = texte.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
    
    # Remplir l'écran de noir
    fenetre.fill(noir)
    
    # Dessiner le message de game over
    fenetre.blit(texte, texte_rect)
    
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


def generer_missile(largeur_fenetre):
    x = random.randint(0, largeur_fenetre - 10)  # Assurer que le missile reste dans les limites de la fenêtre
    y = 0
    vitesse_x = random.uniform(-0.1, 0.1)
    vitesse_y = random.uniform(0.1, 0.4)
    return Missile(x, y, vitesse_x, vitesse_y)

