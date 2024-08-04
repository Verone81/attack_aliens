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

# Le niveau du jeu
niveau_missile = 1
niveau_avant = 1

# Nombre d'essais
essais = 5

# Score initial
score = 0

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(3)

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


#  Initialisation du son
son_bouton_a = pygame.mixer.Sound("audio/click.mp3")
son_tire = pygame.mixer.Sound("audio/tire.mp3")
son_explosion = pygame.mixer.Sound("audio/explosion.mp3")
son_musique = pygame.mixer.music.load('audio/musique.mp3')
son_game_over = pygame.mixer.Sound("audio/game-over.mp3")
son_level = pygame.mixer.Sound("audio/level_suivant.mp3")
son_gagner = pygame.mixer.Sound("audio/gagner.mp3")

pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

canal_tir = pygame.mixer.Channel(0)  # Canal 0 pour le son de tir
canal_explosion = pygame.mixer.Channel(1)  # Canal 1 pour le son d'explosion
canal_game_over = pygame.mixer.Channel(2) # Canal 3 pour le son de game over
canal_gagner = pygame.mixer.Channel(2) # Canal 3 pour le son de game over


# Afficher l'écran de départ et attendre le début du jeu
attendre_commencer(fenetre, fenetre_largeur, fenetre_hauteur, son_bouton_a, manette)

# Événement personnalisé pour générer des missiles ennemis
GENERATE_MISSILE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATE_MISSILE_EVENT, random.randint(1000, 2000))

# Police pour afficher les essais restants
police_essais = pygame.font.Font(None, 36)

# Créer un objet Clock pour limiter le FPS
clock = pygame.time.Clock()
fps = 60  # Limiter à 60 images par seconde

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == GENERATE_MISSILE_EVENT:
            missile = generer_missile(fenetre_largeur, niveau_missile)
            missiles.append(missile)
       

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
                canal_tir.play(son_tire)
                projectiles.append(projectile)
        if boutons[1]: # bouton B
            print("c'est le bouton 1")

    # Remplir l'écran de noir
    fenetre.fill(noir)

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
                canal_explosion.play(son_explosion)
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
                pygame.mixer.music.stop()
                pygame.time.delay(1000)
                canal_game_over.play(son_game_over)
                afficher_game_over(fenetre, fenetre_largeur, fenetre_hauteur)  # Afficher l'écran de game over
    
    # Vérifier les collisions avec la bord bas de l'écran
    for missile in missiles[:]:
        missile.update()
        if missile.is_out_of_bounds(fenetre_hauteur):
            canal_explosion.play(son_explosion)
            missiles.remove(missile)
            essais -= 1
            if essais <= 0:
                pygame.mixer.music.stop()
                pygame.time.delay(1000)
                canal_game_over.play(son_game_over)
                afficher_game_over(fenetre, fenetre_largeur, fenetre_hauteur, score)  # Afficher l'écran de game over

    # Determiner le niveau
    if score >= 10 and score < 20:
        niveau_missile = 2
    elif score >= 20 and score < 30:
        niveau_missile = 3
    elif score >= 30:
        pygame.mixer.music.stop()
        pygame.time.delay(1000)
        canal_gagner.play(son_gagner)
        gagner(fenetre, score, fenetre_largeur, fenetre_hauteur)

    # Si le niveau augmente jouer un son une fois
    if niveau_missile != niveau_avant:
        son_level.play(maxtime=1000)
        niveau_avant += 1

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
    
    # Limiter la vitesse du jeu à 60 FPS
    clock.tick(fps)
0