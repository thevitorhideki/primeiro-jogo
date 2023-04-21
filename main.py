import pygame
from sys import exit


def display_score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score = font.render(f'Score: {current_score}', False, (64, 64, 64))
    score_rect = score.get_rect(center=(WIDTH / 2, 50))
    screen.blit(score, score_rect)

    return current_score


WIDTH = 800
HEIGHT = 400
playing = False
start_time = 0
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load('assets/Sky.png').convert()
ground = pygame.image.load('assets/ground.png').convert()

game_name = font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(WIDTH / 2, 50))

restart = font.render('Press space to run', False, (111, 196, 169))
restart_rect = restart.get_rect(center=(WIDTH / 2, 350))

snail = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail_rect = snail.get_rect(bottomright=(800, HEIGHT - 100))

player = pygame.image.load('assets/Player/player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))

player_name = font.render('Caio', True, 'Black')
player_name_rect = player_name.get_rect(midbottom=(player_rect.midtop))

player_stand = pygame.image.load(
    'assets/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(
    player_stand, (player_stand.get_width() * 2, player_stand.get_height() * 2))
player_stand_rect = player_stand.get_rect(
    center=(WIDTH / 2, HEIGHT / 2))

player_gravity = 0
turn_around = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if playing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
                if event.key == pygame.K_a and turn_around:
                    player = pygame.transform.flip(player, True, False)
                    turn_around = False
                if event.key == pygame.K_d and turn_around == False:
                    player = pygame.transform.flip(player, True, False)
                    turn_around = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                playing = True
                snail_rect.right = 800
                player_rect.left = 80
                player_name_rect.left = 80
                start_time = int(pygame.time.get_ticks() / 1000)

    if playing:
        # Background
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

        # Score
        score = display_score()

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
        if keys[pygame.K_d]:
            player_rect.x += 3
            player_name_rect.x += 3

        # Collision
        if snail_rect.colliderect(player_rect):
            playing = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        total_score = font.render(
            f'Total Score: {score}', False, (111, 196, 169))
        total_score_rect = total_score.get_rect(center=(WIDTH / 2, 50))
        if score == 0:
            screen.blit(game_name, game_name_rect)
        else:
            screen.blit(total_score, total_score_rect)
        screen.blit(restart, restart_rect)

    pygame.display.update()
    clock.tick(60)
