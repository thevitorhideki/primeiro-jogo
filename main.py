import pygame
from sys import exit

WIDTH = 800
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load('assets/Sky.png').convert_alpha()
ground = pygame.image.load('assets/ground.png').convert_alpha()
text = font.render("Lesma (Fofinha) Andando", True, 'green')

snail = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_x_pos = 800

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, HEIGHT - 100))
    screen.blit(text, (220, 50))
    snail_x_pos -= 2
    if snail_x_pos < -100:
        snail_x_pos = 800
    screen.blit(snail, (snail_x_pos, HEIGHT - 135))

    pygame.display.update()
    clock.tick(60)
