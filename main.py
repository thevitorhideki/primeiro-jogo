import pygame
from sys import exit
from random import randint


def display_score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score = font.render(f'Score: {current_score}', False, (64, 64, 64))
    score_rect = score.get_rect(center=(WIDTH / 2, 50))
    screen.blit(score, score_rect)

    return current_score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 5
            if obstacle.bottom == 300:
                screen.blit(snail, obstacle)
            else:
                screen.blit(fly, obstacle)

        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list

    return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True


def player_animation():
    global player, player_index

    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        player = player_walk[int(player_index % len(player_walk))]


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

# Snail
snail1 = pygame.image.load('assets/snail/snail1.png').convert_alpha()
snail2 = pygame.image.load('assets/snail/snail2.png').convert_alpha()
snail_frames = [snail1, snail2]
snail_index = 0
snail = snail_frames[snail_index]

# Fly
fly1 = pygame.image.load('assets/Fly/Fly1.png').convert_alpha()
fly2 = pygame.image.load('assets/Fly/Fly2.png').convert_alpha()
fly_frames = [fly1, fly2]
fly_index = 0
fly = fly_frames[fly_index]

obstacle_rect_list = []

player_wal1 = pygame.image.load(
    'assets/Player/player_walk_1.png').convert_alpha()
player_wal2 = pygame.image.load(
    'assets/Player/player_walk_2.png').convert_alpha()
player_walk = [player_wal1, player_wal2]
player_index = 0
player_jump = pygame.image.load('assets/Player/jump.png').convert_alpha()

player = player_walk[player_index]
player_rect = player_wal1.get_rect(midbottom=(80, 300))
player_gravity = 0

player_name = font.render('Caio', True, 'Black')
player_name_rect = player_name.get_rect(midbottom=(player_rect.midtop))

player_stand = pygame.image.load(
    'assets/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(
    player_stand, (player_stand.get_width() * 2, player_stand.get_height() * 2))
player_stand_rect = player_stand.get_rect(
    center=(WIDTH / 2, HEIGHT / 2))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 300)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if playing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(
                        fly.get_rect(bottomright=(randint(900, 1100), 210)))
                else:
                    obstacle_rect_list.append(
                        snail.get_rect(bottomright=(randint(900, 1100), 300)))
            if event.type == snail_timer:
                snail_index += 1
                snail = snail_frames[int(snail_index % len(snail_frames))]
            if event.type == fly_timer:
                fly_index += 1
                fly = fly_frames[int(fly_index % len(fly_frames))]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                playing = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if playing:
        # Background
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

        # Score
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        player_name_rect.y += player_gravity
        if player_rect.bottom >= 300 and player_name_rect.bottom >= player_rect.midtop[1]:
            player_rect.bottom = 300
            player_name_rect.bottom = player_rect.midtop[1]
            player_gravity = 0

        player_animation()
        screen.blit(player, player_rect)
        screen.blit(player_name, player_name_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        playing = collisions(player_rect, obstacle_rect_list)
    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_name_rect.midbottom = (80, 290)
        player_gravity = 0
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
