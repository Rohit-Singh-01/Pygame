import pygame
import math
import random
from pygame import mixer

pygame.init()

# Create a window ((width, height))
screen = pygame.display.set_mode((800, 600))


# background
background = pygame.image.load("background.jpg")

#background music
mixer.music.load('background.mp3')
mixer.music.play(-1)

#Title and icon 
pygame.display.set_caption("Space Survival")
icon = pygame.image.load("image.png")
pygame.display.set_icon(icon)


#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',35)

textX = 10 
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(X,Y):
    score =font.render("SCORE :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(X,Y))

def game_over_text(X,Y):
    over_text = over_font.render("GAME OVER",True,(255,0,255))
    screen.blit(over_text,(200,250))

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0



#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append (pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append (random.randint(50,150))
    enemyX_change.append (0.3)
    enemyY_change.append (40)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.3
bullet_state = "ready" # ready = bullet is r  eady
                       # fire = firing bullet

# blit means to draw or take as input
# its going to copy the content of one surface to another surface
def player(X,Y):
    screen.blit(playerImg, (X,Y))

def enemy(X,Y,i):
    screen.blit(enemyImg[i], (X,Y))    

def fire_bullet(X,Y):
    global bullet_state
     
    bullet_state = "fire"
    screen.blit(bulletImg,(X + 16, Y + 10))

def collision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False       



# Run the game loop
running = True
while running:

     
    # Fill the screen with a white background ,should be inside the infinite loop becpz it should be visible countinuously until QUIT
    # three values are R(red),G(green),B(blue) becoz every colouris made of this three
    screen.fill((0, 0, 0))
    
    #background image
    screen.blit(background,(0,0))

        #this print fun print  the values of coordinate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed check weather its right or left
    if event.type ==pygame.KEYDOWN:
        #print("a key is pressed")

        if event.key == pygame.K_LEFT:
            playerX_change = -0.6
            #print("left arrow is pressed")
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.6  
            #print("right arrow is pressed") 
  
    if event.type ==pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            if bullet_state is "ready":
                bullet_sound = mixer.Sound('laser.mp3')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
                #print("bullet")


    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
            #print("keystroke is released")
              

    
   ## checking for boundaries of player and enemy 
    playerX += playerX_change  


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736    # the reason 736 is spaceship width is 64 so 800-64 = 736 to stop at border not beyond border
     
     ## enemy movement
    for i in range(num_of_enemy):

        #game over
        if enemyY[i] > 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text(200,250)
            break     


        enemyX[i] += enemyX_change[i]  
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #collosion
        iscollision = collision(enemyX[i], enemyY[i],bulletX, bulletY)
        if iscollision:
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #print(Score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
    
        enemy(enemyX[i], enemyY[i], i)
        #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    

    player(playerX,playerY)
    show_score(textX,textY)
     # Update the display so the R,G,B will be visible game window 
    pygame.display.flip()

# Quit Pygame
pygame.quit()
