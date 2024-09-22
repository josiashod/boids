#!env/bin/python3

import pygame

from boid import *

# pygame setup
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Boids")
running = True
clock = pygame.time.Clock()

# Initialisation des boids
boids = [boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(30)]

def dessiner(boid, screen):
    # Triangle de base
        taille = 8
        angle = math.atan2(boid.velocite[1], boid.velocite[0]) #angle de direction du boid
        points = [
            (boid.position[0] + taille * math.cos(angle), boid.position[1] + taille * math.sin(angle)),
            (boid.position[0] + taille * math.cos(angle + 2.5), boid.position[1] + taille * math.sin(angle + 2.5)),
            (boid.position[0] + taille * math.cos(angle - 2.5), boid.position[1] + taille * math.sin(angle - 2.5)),
        ]
        pygame.draw.polygon(screen, "black", points)

while running:
    screen.fill("white")  # Efface l'écran
    
    # Événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour et dessiner chaque boid
    for boid in boids:
        boid.regles_boids(boids)  # Applique les règles de cohésion, alignement et séparation
        boid.deplacer(WIDTH - 10, HEIGHT - 10)           # Met à jour la position
        dessiner(boid, screen)      # Dessine le boid à l'écran

    # Mettre à jour l'affichage
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()