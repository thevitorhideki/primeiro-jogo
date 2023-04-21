import pygame
from sys import exit

WIDTH = 800
HEIGHT = 400
playing = True

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load('assets/Sky.png').convert()
ground = pygame.image.load('assets/ground.png').convert()

score = font.render("Score: ", True, (64, 64, 64))
score_rect = score.get_rect(center=(WIDTH / 2, 50))

snail = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_rect = snail.get_rect(bottomright=(800, HEIGHT - 100))

player = pygame.image.load('assets/Player/player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))
player_name = font.render('Caio', True, 'Black')
player_name_rect = player_name.get_rect(midbottom=(player_rect.midtop))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if playing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                playing = True
                snail_rect.right = 800

    if playing:
        # Background
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

        # Score
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        screen.blit(score, score_rect)

        # Snail
        snail_rect.left -= 2
        if snail_rect.right < 0:
            snail_rect.left = 800
        screen.blit(snail, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        player_name_rect.y += player_gravity
        if player_rect.bottom >= 300 and player_name_rect.bottom >= player_rect.midtop[1]:
            player_rect.bottom = 300
            player_name_rect.bottom = player_rect.midtop[1]
            player_gravity = 0

        screen.blit(player, player_rect)
        screen.blit(player_name, player_name_rect)

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_rect.x -= 3
            player_name_rect.x -= 3
        elif keys[pygame.K_d]:
            player_rect.x += 3
            player_name_rect.x += 3

        # Collision
        if snail_rect.colliderect(player_rect):
            playing = False
    else:
        screen.fill('black')

    pygame.display.update()
    clock.tick(60)
