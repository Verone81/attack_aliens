import pygame
import sys
import random
from fonction import *
from classe import *

# Initialisation des dimensions de la fenêtre
fenetre_largeur = 800
fenetre_hauteur = 600

# Définition des couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Liste pour stocker les missiles ennemis et les projectiles du canon
missiles = []
projectiles = []

# Initialisation du canon
canon = Canon(fenetre_largeur, fenetre_hauteur)

# Initialisation de Pygame
pygame.init()

# Initialisation de la manette
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    manette = pygame.joystick.Joystick(0)
    manette.init()
else:
    manette = None

# Création de la fenêtre
fenetre = pygame.display.set_mode((fenetre_largeur, fenetre_hauteur))
pygame.display.set_caption("Attack d'Aliens")

# Afficher l'écran de départ et attendre le début du jeu
attendre_commencer(fenetre, fenetre_largeur, fenetre_hauteur, manette)

# Événement personnalisé pour générer des missiles ennemis
GENERATE_MISSILE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATE_MISSILE_EVENT, random.randint(1000, 2000))

# Police pour afficher les essais restants
police_essais = pygame.font.Font(None, 36)

# Nombre d'essais
essais = 5

# Score initial
score = 0

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == GENERATE_MISSILE_EVENT:
            missile = generer_missile(fenetre_largeur)
            missiles.append(missile)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = canon.tirer()
                if projectile:
                    projectiles.append(projectile)

    # Gestion des entrées de la manette
    if manette:
        axes = [manette.get_axis(i) for i in range(manette.get_numaxes())]
        boutons = [manette.get_button(i) for i in range(manette.get_numbuttons())]

        if axes[0] < -0.5:  # Axe X gauche
            canon.pivoter_gauche()
        if axes[0] > 0.5:   # Axe X droite
            canon.pivoter_droite()
        if boutons[0]:  # Bouton A pour tirer
            projectile = canon.tirer()
            if projectile:
                projectiles.append(projectile)
    else:
        # Vérifier les touches enfoncées pour le mouvement continu du canon
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            canon.pivoter_gauche()
        if touches[pygame.K_RIGHT]:
            canon.pivoter_droite()

    # Remplir l'écran de noir
    fenetre.fill(noir)

    # Vérifier les collisions avec la bord bas de l'écran
    for missile in missiles[:]:
        missile.update()
        if missile.is_out_of_bounds(fenetre_hauteur):
            missiles.remove(missile)
            essais -= 1
            if essais <= 0:
                afficher_game_over(fenetre, fenetre_largeur, fenetre_hauteur)  # Afficher l'écran de game over

    # Mettre à jour et dessiner les projectiles du canon
    for projectile in projectiles[:]:
        if not projectile.update():
            projectiles.remove(projectile)
        else:
            projectile.update()

    # Vérifier les collisions entre les projectiles du canon et les missiles ennemis
    for projectile in projectiles[:]:
        for missile in missiles[:]:
            if projectile.collide_with(missile):
                missiles.remove(missile)
                projectiles.remove(projectile)
                score += 1  # Incrémenter le score lorsqu'un missile est détruit
                break

    # Vérifier les collisions entre les missiles ennemis et le canon
    for missile in missiles[:]:
        if missile.collide_with(canon):
            essais -= 1
            missiles.remove(missile)
            if essais <= 0:
                afficher_game_over(fenetre, fenetre_largeur, fenetre_hauteur)  # Afficher l'écran de game over

    # Dessiner les missiles ennemis et les projectiles du canon
    for missile in missiles:
        missile.draw(fenetre)
    for projectile in projectiles:
        projectile.draw(fenetre)

    # Dessiner le canon
    canon.draw(fenetre)

    # Afficher les essais restants
    surface_essais = police_essais.render(f'Essais: {essais}', True, blanc)
    fenetre.blit(surface_essais, (10, 10))

    # Afficher le score
    afficher_score(fenetre, score)

    # Mettre à jour l'affichage
    pygame.display.flip()
