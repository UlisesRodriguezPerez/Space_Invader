import math
import random

import pygame
from pygame import mixer


class Game:
    screen = None
    
    def __init__(self, width, height):
        # Intialize the pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        # create the screen
        
        # Background
        self.background = pygame.image.load('background.png')

        # Sound
        mixer.music.load("background.wav")
        mixer.music.play(-1)

        # Caption and Icon
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)
        
        # Initialize the Clases
        self.enemy = Enemy()
        self.player = Player()
        self.bullet = Bullet()
        self.score = Score()
        self.game_over = GameOver()
        
        # Game Loop
        self.running = True
        while self.running:
            
            # RGB = Red, Green, Blue
            self.screen.fill((0, 0, 0))
            # Background Image
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # if keystroke is pressed check whether its right or left
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        self.player.playerX_change = 5
                    if event.key == pygame.K_SPACE:
                        if self.bullet.bullet_state == "ready":
                            self.bullet.bulletSound = mixer.Sound("laser.wav")
                            self.bullet.bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            self.bullet.bulletX = self.player.playerX
                            self.bullet.fire_bullet(self,self.bullet.bulletX, self.bullet.bulletY)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.playerX_change = 0

            # 5 = 5 + -0.1 -> 5 = 5 - 0.1
            # 5 = 5 + 0.1

            self.player.playerX += self.player.playerX_change
            if self.player.playerX <= 0:
                self.player.playerX = 0
            elif self.player.playerX >= 736:
                self.player.playerX = 736
            
            
            
            # Enemy Movement
            for i in range(self.enemy.num_of_enemies):
                # Game Over
                if self.enemy.enemyY[i] > 440:
                    for j in range(self.enemy.num_of_enemies):
                        self.enemy.enemyY[j] = 2000
                    self.game_over.game_over_text(self)
        
                    break

                self.enemy.enemyX[i] += self.enemy.enemyX_change[i]
                if self.enemy.enemyX[i] <= 0:
                    self.enemy.enemyX_change[i] = 4
                    self.enemy.enemyY[i] += self.enemy.enemyY_change[i]
                elif self.enemy.enemyX[i] >= 736:
                    self.enemy.enemyX_change[i] = -4
                    self.enemy.enemyY[i] += self.enemy.enemyY_change[i]

                # Collision
                
                collision = self.bullet.isCollision(self.enemy.enemyX[i], self.enemy.enemyY[i], self.bullet.bulletX, self.bullet.bulletY)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.bullet.bulletY = 480
                    self.bullet.bullet_state = "ready"
                    self.score.score_value += 1
                    self.enemy.enemyX[i] = random.randint(0, 736)
                    self.enemy.enemyY[i] = random.randint(50, 150)

                self.enemy.enemy(self,self.enemy.enemyX[i], self.enemy.enemyY[i], i)

            # Bullet Movement
            if self.bullet.bulletY <= 0:
                self.bullet.bulletY = 480
                self.bullet.bullet_state = "ready"

            if self.bullet.bullet_state == "fire":
                self.bullet.fire_bullet(self,self.bullet.bulletX, self.bullet.bulletY)
                self.bullet.bulletY -= self.bullet.bulletY_change

            self.player.player(self,self.player.playerX, self.player.playerY)
            self.score.show_score(self,self.score.textX, self.score.testY)
            pygame.display.update()

        pygame.quit()
        
    # Player
class Player: 
    def __init__(self):
        self.playerImg = pygame.image.load('player.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0

    def player(self,game,x, y):
        game.screen.blit(self.playerImg, (x, y))
    
class Bullet: # Bullet
    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    def __init__(self):
        self.bulletImg = pygame.image.load('bullet.png')
        self.bulletX = 0
        self.bulletY = 480
        self.bulletX_change = 0
        self.bulletY_change = 10
        self.bullet_state = "ready"
    
    def fire_bullet(self,game,x, y):

        self.bullet_state = "fire"
        game.screen.blit(self.bulletImg, (x + 16, y + 10)) 

    def isCollision(self,enemyX,enemyY,bulletX,bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    #Enemy
class Enemy: 
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    
    def __init__(self):
        for i in range(Enemy.num_of_enemies):
            self.enemyImg.append(pygame.image.load('enemy.png'))
            self.enemyX.append(random.randint(0, 736))
            self.enemyY.append(random.randint(50, 150))
            self.enemyX_change.append(4)
            self.enemyY_change.append(40)
       
    def enemy(self,game,x, y, i):
        game.screen.blit(self.enemyImg[i], (x, y))    
        
    # Score 
class Score:
    def __init__(self):
        self.score_value = 0
        self.textX = 10
        self.testY = 10
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    
    def show_score(self,game,x, y):
        score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        game.screen.blit(score, (x, y))
        
    # Game Over
class GameOver: 
    def __init__(self):
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        
    def game_over_text(self,game):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        game.screen.blit(over_text, (200, 250))

if __name__ == '__main__':
    game = Game(800, 600)