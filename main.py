import pygame
from sys import exit

WIDTH = 800
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load('assets/Sky.png').convert()
ground = pygame.image.load('assets/ground.png').convert()

snail = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_rect = snail.get_rect(bottomright=(800, HEIGHT - 100))

player = pygame.image.load('assets/Player/player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, HEIGHT - 100))
    snail_rect.left -= 2
    if snail_rect.right < 0:
        snail_rect.left = 800
    screen.blit(snail, snail_rect)
    screen.blit(player, player_rect)

    pygame.display.update()
    clock.tick(60)
