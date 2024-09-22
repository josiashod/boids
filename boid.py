#!env/bin/python3

import random
import math

class boid:
    def __init__(self, x, y):
        # Initialiser la position et la vélocité aléatoires
        self.position = [x, y]
        self.velocite = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.max_speed = 4  # Vitesse maximale du boid
        self.max_force = 0.05  # Force maximale appliquée

    def deplacer(self, WIDTH = 0, HEIGHT = 0):
        """Met à jour la position du boid en fonction de sa vélocité."""

        self.position[0] += self.velocite[0]
        self.position[1] += self.velocite[1]

        # Si le boid atteint le bord gauche ou droit, inverser la vélocité en X
        if self.position[0] <= 10 or self.position[0] >= WIDTH:
            self.velocite[0] *= -1  # Inverser la direction sur l'axe X

        # Si le boid atteint le bord supérieur ou inférieur, inverser la vélocité en Y
        if self.position[1] <= 10 or self.position[1] >= HEIGHT:
            self.velocite[1] *= -1  # Inverser la direction sur l'axe Y


    def appliquer_force(self, force):
        """Ajoute une force à la vélocité actuelle."""
        self.velocite[0] += force[0]
        self.velocite[1] += force[1]

        # Limiter la vitesse maximale
        self.limiter_vitesse()

    def limiter_vitesse(self):
        """Limite la vitesse du boid à sa vitesse maximale."""
        vitesse = math.sqrt(self.velocite[0]**2 + self.velocite[1]**2)
        if vitesse > self.max_speed:
            self.velocite[0] = (self.velocite[0] / vitesse) * self.max_speed
            self.velocite[1] = (self.velocite[1] / vitesse) * self.max_speed

    def cohesion(self, boids):
        """Calcule la force de cohésion, attirant le boid vers le centre de ses voisins."""
        perception_radius = 60
        centre_masse = [0, 0]
        total = 0
        for boid in boids:
            distance = self.distance(boid.position)
            # on calcule le centre de masse avec les voisins detecté
            if boid != self and distance < perception_radius:
                centre_masse[0] += boid.position[0]
                centre_masse[1] += boid.position[1]
                total += 1
        if total > 0:
            # si des voisins on effectivement été detecté on applique une force pour ce diriger dans la direction du centre de masse
            centre_masse[0] /= total
            centre_masse[1] /= total
            direction = [centre_masse[0] - self.position[0], centre_masse[1] - self.position[1]]
            direction = self.normaliser(direction)
            return self.appliquer_limite(direction)
        return [0, 0]

    def alignement(self, boids):
        """Calcule la force d'alignement, faisant que le boid s'aligne avec la vélocité moyenne des voisins."""
        perception_radius = 60
        velocite_moyenne = [0, 0]
        total = 0
        for boid in boids:
            distance = self.distance(boid.position)
            if boid != self and distance < perception_radius:
                velocite_moyenne[0] += boid.velocite[0]
                velocite_moyenne[1] += boid.velocite[1]
                total += 1
        if total > 0:
            velocite_moyenne[0] /= total
            velocite_moyenne[1] /= total
            velocite_moyenne = self.normaliser(velocite_moyenne)
            return self.appliquer_limite(velocite_moyenne)
        return [0, 0]

    def separation(self, boids):
        """Calcule la force de séparation, évitant les collisions entre boids."""
        perception_radius = 45
        force_repulsion = [0, 0]
        total = 0
        for boid in boids:
            distance = self.distance(boid.position)
            if boid != self and distance < perception_radius:
                repulsion = [self.position[0] - boid.position[0], self.position[1] - boid.position[1]]
                repulsion = self.normaliser(repulsion)
                force_repulsion[0] += repulsion[0] / distance  # Plus proche -> plus forte répulsion
                force_repulsion[1] += repulsion[1] / distance
                total += 1
        if total > 0:
            force_repulsion[0] /= total
            force_repulsion[1] /= total
            return self.appliquer_limite(force_repulsion)
        return [0, 0]

    def appliquer_limite(self, force):
        """Limite l'intensité de la force appliquée."""
        magnitude = math.sqrt(force[0]**2 + force[1]**2)
        if magnitude > self.max_force:
            force[0] = (force[0] / magnitude) * self.max_force
            force[1] = (force[1] / magnitude) * self.max_force
        return force

    def normaliser(self, vecteur):
        """Normalise un vecteur (le ramène à une magnitude de 1)."""
        magnitude = math.sqrt(vecteur[0]**2 + vecteur[1]**2)
        if magnitude > 0:
            return [vecteur[0] / magnitude, vecteur[1] / magnitude]
        return [0, 0]

    def distance(self, autre_position):
        """Calcule la distance euclidienne entre deux points."""
        return math.sqrt((self.position[0] - autre_position[0])**2 + (self.position[1] - autre_position[1])**2)

    def regles_boids(self, boids):
        """Applique les trois règles des Boids (cohésion, alignement, séparation)."""
        force_cohesion = self.cohesion(boids)
        force_alignement = self.alignement(boids)
        force_separation = self.separation(boids)

        # Combiner les forces et appliquer les à la vélocité
        self.appliquer_force(force_cohesion)
        self.appliquer_force(force_alignement)
        self.appliquer_force(force_separation)

