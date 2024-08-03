import pygame
import math
import random

class Missile:
    def __init__(self, x, y, vitesse_x, vitesse_y):
        self.x = x
        self.y = y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.width = 5
        self.height = 5
        self.color = (255, 0, 0)  # Rouge
        self.trail = []

    def update(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10500:
            self.trail.pop(0)

    def draw(self, screen):
        for pos in self.trail:
            pygame.draw.rect(screen, self.color, (pos[0], pos[1], self.width, self.height))

    def is_out_of_bounds(self, hauteur_fenetre):
        # Vérifier si le missile dépasse le bas de l'écran
        return self.y > hauteur_fenetre


    def collide_with(self, other=None):
        # Vérifier les collisions avec un autre objet
        if other:
            return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
                pygame.Rect(other.x, other.y, other.width, other.height)
            )
        
        return False



class Canon:
    def __init__(self, largeur_fenetre, hauteur_fenetre):
        self.largeur_fenetre = largeur_fenetre
        self.hauteur_fenetre = hauteur_fenetre
        self.image = pygame.image.load('images/canon.png')
        self.largeur = self.image.get_width()
        self.hauteur = self.image.get_height()
        self.x = largeur_fenetre / 2 - self.largeur / 2
        self.y = hauteur_fenetre - self.hauteur
        self.vitesse = 5
        self.angle = 0  # Angle initial de rotation du canon (vers le haut)

    def pivoter_gauche(self):
        self.angle += 0.1
        if self.angle >= 360:
            self.angle -= 360

    def pivoter_droite(self):
        self.angle -= 0.1
        if self.angle < 0:
            self.angle += 360

    def tirer(self):
        angle_radians = math.radians(self.angle + 90)
        vitesse_x = math.cos(angle_radians) * 5
        vitesse_y = -math.sin(angle_radians) * 5
        return Projectile(self.x + self.largeur / 2, self.y, vitesse_x, vitesse_y)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)
        self.width = new_rect.width  # Ajout de l'attribut width
        self.height = new_rect.height  # Ajout de l'attribut height

class Projectile:
    def __init__(self, x, y, vitesse_x, vitesse_y):
        self.x = x
        self.y = y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.width = 3
        self.height = 10
        self.color = (0, 255, 0)  # Vert

    def update(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide_with(self, other):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(other.x, other.y, other.width, other.height))
