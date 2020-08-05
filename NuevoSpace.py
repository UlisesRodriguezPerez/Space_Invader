import math
import random

import pygame
from pygame import mixer

    #Clase Game( principal).
class Game:
    screen = None
    #   Inicialización del juego.
    def __init__(self, width, height):
        # Intialize the pygame
        pygame.init()
        #   Create the screen.
        self.screen = pygame.display.set_mode((width, height))
        #   Sound
        self.sound()
        #   Caption and Icon.
        self.caption_and_icon()
        #   Initialize the Clases.
        self.inicializar()
        #   Game Loop.
        self.run_game()
        pygame.quit()

    #   Función que se encarga de mantener el juego corriendo.
    def run_game(self):
        self.running = True
        
        while self.running:
            #   RGB = Red, Green, Blue.
            self.screen.fill((0, 0, 0))
            #   Background Image
            self.screen.blit(self.background, (0, 0))
            #   Acción de las teclas.
            self.event_type()
            #   validar campos del player.
            self.player_validation()
            #   Enemy Movement.
            self.enemy_Movement()
            #   Bullet Movement.
            self.bullet_movement()
            #   Actualizar jugador.
            self.player.set_player(self,self.player.playerX, self.player.playerY)
            #   Actualizar Puntuación.
            self.score.show_score(self,self.score.textX, self.score.testY)
            #   Actualiza las vidas de la pantalla.
            self.lifes.show_lifes(self,self.lifes.textX,self.lifes.textY)
            #   Actualiza el nivel de la pantalla.
            self.level_of_game.shoe_level(self,self.level_of_game.textX,self.level_of_game.textY)
            #  Actualiza todo el mostrado.
            pygame.display.update()

    # Función encargada del sonido.
    def sound(self):
        mixer.music.load("background.wav")
        mixer.music.play(-1)

    #   Función que se encarga de cargar los iconos.
    def caption_and_icon(self):
        #   Inicia el fondo del juego.
        self.background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)

    #Función que inicializa todas las clases.
    def inicializar(self):
        self.enemy = Enemy()
        self.player = Player()
        self.bullet = Bullet()
        self.score = Score()
        self.game_over = GameOver()
        self.level_of_game = Level()
        self.lifes = Life()

    #   Función para ver qué accion debe hacer el programa según la tecla presionada.
    def event_type(self):
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

    #   Valida los campos del player, para que no se salga de la pantalla.
    def player_validation(self):
        self.player.playerX += self.player.playerX_change
        if self.player.playerX <= 0:
            self.player.playerX = 0
        elif self.player.playerX >= 736:
            self.player.playerX = 736

    #   Todo el movimiento del enemigo.
    def enemy_Movement(self):
        #print(self.enemy.num_of_enemies)
        for i in range(self.enemy.num_of_enemies):
            # Game Over
            if self.enemy.enemyY[i] > 440:
                if self.lifes.lifes_of_level != 1:
                    self.lifes.lifes_of_level = self.lifes.lifes_of_level - 1
                    self.enemy.enemyY[i] = 50 
                    
                else:
                    for j in range(self.enemy.num_of_enemies):
                        self.enemy.enemyY[j] = 2000
                    self.game_over.game_over_text(self)
                    break
            self.enemy.enemyX[i] += self.enemy.enemyX_change[i]
            #   Enemy movement
            self.enemy_direction(i)
            # Collision
            collision = self.bullet.isCollision(self.enemy.enemyX[i], self.enemy.enemyY[i], self.bullet.bulletX, self.bullet.bulletY)
            if collision:
                #   Cuando colisuona realiza cambios en el juego. Retorna la nueva ubicación del enemigo.   REVISAR
                self.colision(i)
                #   Returna a enemy_Movement para actualizar los indices.
                return self.enemy_Movement()
                
            #   Actualiza el enemigo.
            else:
                self.enemy.enemy(self,self.enemy.enemyX[i], self.enemy.enemyY[i], i)
             

    # Bullet Movement.
    def bullet_movement(self):
        if self.bullet.bulletY <= 0:
            self.bullet.bulletY = 480
            self.bullet.bullet_state = "ready"

        if self.bullet.bullet_state == "fire":
            self.bullet.fire_bullet(self,self.bullet.bulletX, self.bullet.bulletY)
            self.bullet.bulletY -= self.bullet.bulletY_change

    #   Función para cambios cuando colisiona. 
    def colision(self,i):
        suma = 0
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        self.bullet.bulletY = 480
        self.bullet.bullet_state = "ready"
        suma = self.clasificar_enemy(i)
        self.score.score_value += suma
        #   Función que se encarga de destruir el enemigo y crear la explosión.
        self.destruir_enemigo(i)
        puntaje = self.score.score_value
        if puntaje % 10 == 0:           #   Obtiene una vida cada que sume 10 puntos.
            self.lifes.lifes_of_level += 1
        if self.enemy.num_of_enemies == 0:
            #   pasa al siguiente nivel.
            self.siguiente_nivel()
            self.level_of_game.level += 1
    def clasificar_enemy(self,i):
        #REVISAR pendiente ver cómo commparar imagenes.
        if self.enemy.enemyImg[i] == pygame.image.load('enemy0.png'):
            return 1
        elif self.enemy.enemyImg[i] == pygame.image.load('enemy1.png'):
            return 2
        else:
            return 1

    def destruir_enemigo(self,i):
        self.enemy.enemyImg[i] = pygame.image.load('explosion.png')
        self.enemy.enemy(self,self.enemy.enemyX[i], self.enemy.enemyY[i], i)
        self.enemy.enemyX.pop(i)
        self.enemy.enemyY.pop(i)
        self.enemy.enemyX_change.pop(i)
        self.enemy.enemyY_change.pop(i)
        self.enemy.enemyImg.pop(i)
        self.enemy.num_of_enemies = self.enemy.num_of_enemies - 1

    #   Función encargada de aumentar los enemigos cuando se acaben.
    def siguiente_nivel(self):
        
        #   Carga nuevamente los enemigos.
        self.enemy.num_of_enemies_leves = self.enemy.num_of_enemies_leves + 1
        self.enemy.num_of_enemies = self.enemy.num_of_enemies_leves
        for i in range(self.enemy.num_of_enemies_leves):
            self.enemy.generar_enemy()
            # self.enemy.enemy(self,self.enemy.enemyX[i], self.enemy.enemyY[i], i)
        
        
        return self.enemy_Movement()

    #   Función para cambiar de dirección el enemigo.
    def enemy_direction(self,i):
        if self.enemy.enemyX[i] <= 0:
            self.enemy.enemyX_change[i] = 4
            self.enemy.enemyY[i] += self.enemy.enemyY_change[i]
        elif self.enemy.enemyX[i] >= 736:
            self.enemy.enemyX_change[i] = -4
            self.enemy.enemyY[i] += self.enemy.enemyY_change[i]

    # Clase Player
class Player: 
    #   Constructor de la clase.
    def __init__(self):
        self.playerImg = pygame.image.load('player.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0

    #   Función para actualizar el player.
    def set_player(self,game,x, y):
        game.screen.blit(self.playerImg, (x, y))

    #   Clase Bullet.
class Bullet: # Bullet
    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    #   Constructor de la clase.
    def __init__(self):
        self.bulletImg = pygame.image.load('bullet.png')
        self.bulletX = 0
        self.bulletY = 480
        self.bulletX_change = 0
        self.bulletY_change = 10
        self.bullet_state = "ready"
        self.bullet_range = 16
    
    #   Cambia el estado a disparar.
    def fire_bullet(self,game,x, y):
        self.bullet_state = "fire"
        game.screen.blit(self.bulletImg, (x + self.bullet_range, y + 10)) 

        #game.screen.blit(self.bulletImg, (x - self.bullet_range, y + 10)) 
        # game.screen.blit(self.bulletImg, (x + self.bullet_range, y + 10)) 
        # game.screen.blit(self.bulletImg, (x + self.bullet_range, y + 10)) 

    #   Función booleana para saber si la bala colicionó.
    def isCollision(self,enemyX,enemyY,bulletX,bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False


    #Clase Enemy.
class Enemy: 
    #   Atributos de la clase.
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 3
    num_of_enemies_leves = 3

    #   Constructor de la clase.
    def __init__(self):
        #   Recorre la cantidad de enemigos para crearlos.
        for i in range(Enemy.num_of_enemies):
            self.generar_enemy()
    def generar_enemy(self):
        enemy_random = random.randint(0, 2)
        self.enemyImg.append(pygame.image.load('enemy'+ str(enemy_random)+'.png'))
        self.enemyX.append(random.randint(0, 736))
        self.enemyY.append(random.randint(50, 150))
        self.enemyX_change.append(4)
        self.enemyY_change.append(40)
    #   Función para ir mostrando cada enemigo.
    def enemy(self,game,x, y, i):       #REVISAR cambiar nombre a la función.
        game.screen.blit(self.enemyImg[i], (x, y))    
        
    #   Clase vidas.
class Life:
    #   Constructor de la clase.
    def __init__(self):
        self.lifes_of_level = 3
        self.textX = 200
        self.textY = 10
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    
    #   Función para actualizar las vidas en la pantalla.
    def show_lifes(self,game,x, y):
        lifes = self.font.render("Lifes : " + str(self.lifes_of_level), True, (255, 255, 255))
        game.screen.blit(lifes, (x, y))

    #   Clase que contiene las caracterísiticas acerca de los niveles.
class Level:
    #    Constructor de la clase.
    def __init__(self):
        self.level = 1
        self.textX = 400
        self.textY = 10
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    #   Función para actualizar el nivel en pantalla.
    def shoe_level(self,game,x, y):
        levels = self.font.render("Level : " + str(self.level), True, (255, 255, 255))
        game.screen.blit(levels, (x, y))

    # Clase Score 
class Score:
    #   Constructor de la clase.
    def __init__(self):
        self.score_value = 0
        self.textX = 10
        self.testY = 10
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    
    #   Función para actualizar la puntuación en pantalla.
    def show_score(self,game,x, y):
        score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        game.screen.blit(score, (x, y))
        
    #   Clase Game Over.
class GameOver: 
    #   Constructor de la clase.
    def __init__(self):
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

    #Función para mostrar "GAE OVER" en pantalla.
    def game_over_text(self,game):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        game.screen.blit(over_text, (200, 250))
#   main del programa.
if __name__ == '__main__':
    game = Game(800, 600)