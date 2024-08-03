import pygame
import math

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
        if len(self.trail) > 1000:
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
        self.dernier_tir = 0  # Temps du dernier tir
        self.intervalle_tir = 100  # Intervalle entre les tirs en millisecondes

    def pivoter_gauche(self):
        self.angle += 0.3
        if self.angle >= 360:
            self.angle -= 360

    def pivoter_droite(self):
        self.angle -= 0.3
        if self.angle < 0:
            self.angle += 360

    def tirer(self):
        maintenant = pygame.time.get_ticks()  # Obtenir le temps actuel
        if maintenant - self.dernier_tir >= self.intervalle_tir:
            self.dernier_tir = maintenant
            angle_radians = math.radians(self.angle + 90)
            vitesse_x = math.cos(angle_radians) * 2
            vitesse_y = -math.sin(angle_radians) * 2
            return Projectile(self.x + self.largeur / 2, self.y, vitesse_x, vitesse_y)
        return None

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)
        self.width = new_rect.width  # Ajout de l'attribut width
        self.height = new_rect.height  # Ajout de l'attribut height


class Projectile:
    def __init__(self, x, y, vitesse_x, vitesse_y, max_distance=800):
        self.x = x
        self.y = y
        self.vitesse_x = vitesse_x
        self.vitesse_y = vitesse_y
        self.width = 3
        self.height = 3
        self.color = (0, 255, 0)  # Vert
        self.distance_parcourue = 0
        self.max_distance = max_distance

    def update(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.distance_parcourue += math.sqrt(self.vitesse_x**2 + self.vitesse_y**2)

        # Vérifie si le projectile a dépassé la distance maximale
        if self.distance_parcourue >= self.max_distance:
            return False  # Le projectile doit être supprimé
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide_with(self, other):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(pygame.Rect(other.x, other.y, other.width, other.height))