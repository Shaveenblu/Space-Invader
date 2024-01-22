import pygame
import random
import math
from pygame import mixer

# Python initialize
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# backgroud
background = pygame.image.load('b.jpg')

#BAck gound sound
mixer.music.load('spaceinvaders1.mpeg')
mixer.music.play(-1)

# Caption
pygame.display.set_caption("Space Invaders")

#icon before caption in window
icon = pygame.image.load('001-rocket.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('f-jet.png')
playerx = 370
playery = 480
playerx_chnge = 0

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_chnge = []
enemyy_change = []
num_enemy = 6
for i in range (num_enemy):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,800))
    enemyy.append(random.randint(50,150))
    enemyx_chnge.append(0.2)
    enemyy_change.append(40)

# Ready - Cant see the bullet ob the screen
bulletimg = pygame.image.load('bu.png')
bulletx = 0
bullety = 480
bulletx_chnge = 10
bullety_change = 1.8
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('Dune_Rise.ttf',32)

textX = 10
textY = 10

over_f = pygame.font.Font('Dune_Rise.ttf',48)
def gameOVer():
    overt = over_f.render("GAME OVER : " + str(score_value),True, (25,55,25))
    screen.blit(overt ,(200,250))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (25,55,25))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y):
    screen.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    # x & y are cordinates for the bullet fire lil bit top from the 
    # and lil bit bottom from enemy
    screen.blit(bulletimg,(x + 16,y + 10))

def isCollision(enemyx, enemyy,bulletx,bullety):
    distance = math.sqrt((math.pow(enemyx-enemyy,2)) + (math.pow(enemyy-bullety,2)))
    if distance <27:
        return True
    else:
        return False



# Game loop
running = True
while running:
    # color was used in the begining to 
    # make sure everything is drawn on it
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # if keystroke is pressed check right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_chnge = -0.5
            if event.key == pygame.K_RIGHT:
                playerx_chnge = 0.5

            # Event that handles how the bullet moves
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    b_sound = mixer.Sound('shoot.wav')
                    b_sound.play()
                    # get the current x cordinate of ship
                    bulletx = playerx
                    fire_bullet(bulletx,bullety)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_chnge = 0


    playerx += playerx_chnge

    # if the player hit the boundary
    if playerx <= 0:
        playerx = 0
    elif playerx >=736:
        playerx = 736

    enemyx += enemyx_chnge

    # if the enemy hit the boundary
    for i in range(num_enemy):
        # Game Over
        if enemyy[i] > 440:
            for j in range(num_enemy):
                enemyy[j] = 2000
            gameOVer()
            break


        enemyx[i] += enemyx_chnge[i]
        if enemyx[i] <= 0:
            enemyx_chnge[i] = 0.2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >=736:
            enemyx_chnge[i] = -0.2
            enemyy[i] += enemyy_change[i]
        # Collision & respawn
        collision = isCollision(enemyx[i],enemyy[i],bulletx,bullety)
        if collision:
            ex_sound = mixer.Sound('explosion.wav')
            ex_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0,735)
            enemyy[i] = random.randint(50,150)

        enemy(enemyx[i],enemyy[i])


    # Bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change



    player(playerx,playery)
 
    show_score(textX,textY)

    pygame.display.update()

