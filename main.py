import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('assets/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('assets/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        
        self.player_jump = pygame.image.load('assets/Player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(90, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            self.image = self.player_walk[int(self.player_index % len(self.player_walk))]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('assets/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('assets/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos = 210
        elif type == 'snail':
            snail_1 = pygame.image.load('assets/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('assets/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos = 300
            
        self.animation_index = 0 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self.y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1
        self.image = self.frames[int(self.animation_index % len(self.frames))]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
    def update(self):
        self.animation_state() 
        self.rect.x -= 5
        self.destroy() 

def display_score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score = font.render(f'Score: {current_score}', False, (64, 64, 64))
    score_rect = score.get_rect(center=(WIDTH / 2, 50))
    screen.blit(score, score_rect)

    return current_score

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

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
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background
sky = pygame.image.load('assets/Sky.png').convert()
ground = pygame.image.load('assets/ground.png').convert()

# Menu
game_name = font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(WIDTH / 2, 50))

restart = font.render('Press space to run', False, (111, 196, 169))
restart_rect = restart.get_rect(center=(WIDTH / 2, 350))

player_stand = pygame.image.load('assets/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (player_stand.get_width() * 2, player_stand.get_height() * 2))
player_stand_rect = player_stand.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# Timers
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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))                
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
        player.draw(screen)
        player.update()
        
        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        playing = collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        total_score = font.render(f'Total Score: {score}', False, (111, 196, 169))
        total_score_rect = total_score.get_rect(center=(WIDTH / 2, 50))
        if score == 0:
            screen.blit(game_name, game_name_rect)
        else:
            screen.blit(total_score, total_score_rect)
        screen.blit(restart, restart_rect)

    pygame.display.update()
    clock.tick(60)
