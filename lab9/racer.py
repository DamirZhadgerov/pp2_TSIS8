import pygame
import os
from random import randint

# Set the working directory
os.chdir(r"C:\cbb")

# Initialize Pygame
pygame.init()

# Set the display dimensions
W, H = 400, 600
sc = pygame.display.set_mode((W, H))

# Load background and score images
bg = pygame.image.load('AnimatedStreet.png').convert_alpha()
score_image = pygame.image.load('score_fon.png').convert_alpha()

# Set up font
font = pygame.font.Font(None, 40)

# Set up clock
clock = pygame.time.Clock()

# Define Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, speed, image, score, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.score = score
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 60:
            self.rect.y += self.speed
        else:
            self.kill()

# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, speed, image, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()

# Define coins data
coins_data = [{'path': r'C:\cbb\lemor.png', 'score': 10},  # 3 Coins with different weights
              {'path': r'C:\cbb\rabbit.png', 'score': 15},  
              {'path': r'C:\cbb\panda.png', 'score': 20}]

# Load coin and enemy images
coin_images = [pygame.image.load(data['path']).convert_alpha() for data in coins_data]
enemy_image = pygame.image.load('enemy.png').convert_alpha()
player = pygame.image.load(r'C:\cbb\player.png').convert_alpha()

# Create sprite groups
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Initialize game variables
game_score = 0
coin_spawn_timer = pygame.USEREVENT
pygame.time.set_timer(coin_spawn_timer, 2500)
enemy_speed = 3

# Define player rectangle
player_rect = player.get_rect(centerx=W // 2, bottom=H - 5)

# Define function to create coins
def createCoin(group):
    indx = randint(0, len(coins_data) - 1)
    x = randint(20, W - 20)
    speed = randint(2, 4)
    return Coin(x, speed, coin_images[indx], coins_data[indx]['score'], group)

# Define function to create enemies
def createEnemy(group):
    global enemy_speed
    indx = randint(40, W - 40)
    return Enemy(indx, enemy_speed, enemy_image, group)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == coin_spawn_timer:
            createCoin(coins)
            if randint(1, 2) % 2 == 0:
                createEnemy(enemies)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
        if player_rect.x < 0:
            player_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        player_rect.x += 5
        if player_rect.x > W - player_rect.width:
            player_rect.x = W - player_rect.width

    sc.blit(bg, (0, 0))
    sc.blit(score_image, (0, 0))  # Display score image
    sc_text = font.render(str(game_score), 1, (0, 0, 0))
    sc.blit(sc_text, (20, 15))
    sc.blit(player, player_rect)

    # Check for collisions between player and coins
    for coin in coins:
        if player_rect.colliderect(coin.rect):
            game_score += coin.score
            coin.kill()

    # Update and draw enemies
    enemies.update(H)
    enemies.draw(sc)

    # Update and draw coins
    coins.update(H)
    coins.draw(sc)

    pygame.display.update()
    clock.tick(60)
