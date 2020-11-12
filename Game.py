import pygame # to import modules in pygame
import random # to generate random nums
import os # for fs management
import math # for math functions
from pygame import mixer # for music

# initializes the modules in pygame
pygame.init()

# images
icon = pygame.image.load(os.path.join("assets","window_logo.png"))
player_ship = pygame.image.load(os.path.join("assets","player_ship.png"))

background = pygame.image.load(os.path.join("assets","bg.png"))
bullet = pygame.image.load(os.path.join("assets","bullet.png"))

# player
playerX = 400-32
playerY = 490
player_vel = 1.3

# enemy
enemyX = []
enemyY = []
enemy_vel = []
enemy_changeY = []
num_of_enemies = 7
enemy_invader = []

# background sound
mixer.music.load(os.path.join("music", "bg.wav"))
mixer.music.play(-1) # -1 means loop forever

for i in range(num_of_enemies):
	enemy_choice = random.randint(0,2)
	if enemy_choice == 0:
		enemy_invader.append(pygame.image.load(os.path.join("assets","enemy_invader.png")))
	elif enemy_choice == 1:
		enemy_invader.append(pygame.image.load(os.path.join("assets","enemy2.png")))
	elif enemy_choice == 2:
		enemy_invader.append(pygame.image.load(os.path.join("assets","enemy3.png")))
	enemyX.append(random.randint(0, 735))
	enemyY.append(random.randint(0, 150))
	enemy_vel.append(0.8)
	enemy_changeY.append(45)

# bullet
# "ready" means it is ready
# "firing" the bullet is currently moving
bulletX = 0
bulletY = 490
bullet_vel = 2
bullet_state = "ready"

# FONT STYLES
# score
font = pygame.font.Font('assets\\Janyss Brush.ttf', 40)
# game over
game_over_font = pygame.font.Font("assets\\Janyss Brush.ttf", 68)
scoreX = 10
scoreY = 10
score_value = 0

def show_score(x, y):
	score = font.render("Score: " + str(score_value), True, (255, 255, 255))
	window.blit(score, (x, y))

#create the window and its basic elements
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

def enemy(x, y, i):
	window.blit(enemy_invader[i], (x, y))

def player(x, y):
	#blit is basically "DRAW"
	window.blit(player_ship, (x, y))

def fire_bullet(x, y):
	global bullet_state #the bullet_state variable can now be accessed by functions.
	bullet_state = "firing"
	window.blit(bullet, (x+16, y+10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
	distance  = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
	if distance<27:	
		return True
	else:
		return False

def game_over_text():
	game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
	window.blit(game_over_text, (255, 250))
#the game loop
running = True
while running:

	#RGB - Red, Green and Blue
	#this has to be above everything cuz this draws the first surface
	window.blit(background, (0, 0))
	white = (255, 255, 255)
	pygame.draw.line(window, white,(0, 460), (800, 460), 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			print("Game exit")

	#if keystroke is pressed and checking
	if event.type == pygame.KEYDOWN:  
		if event.key == pygame.K_RIGHT:
			playerX+=player_vel
		if event.key == pygame.K_LEFT:
			playerX-=player_vel
		if event.key == pygame.K_SPACE:
			if bullet_state == "ready":
				bullet_sound = mixer.Sound('music\\laser.wav')
				bullet_sound.play()
				bulletX = playerX
				fire_bullet(bulletX, bulletY)

	#boundary check for player
	if playerX <= 0:
		playerX = 0
	if playerX >= 800-64:
		playerX = 800-64

	for i in range(num_of_enemies):

		# game over code
		if enemyY[i] >= 450:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemy_vel[i]

		if enemyX[i] <= 0:
			enemyY[i]+=enemy_changeY[i]
			enemy_vel[i] = 0.8  # '+' for moving right
		if enemyX[i] >= 800-64:
			enemyY[i]+=enemy_changeY[i]
			enemy_vel[i] = -0.8 # '-' for moving left


		# collison check
		collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			death_sound = mixer.Sound('music\\death1.wav')
			death_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value+=1
			enemyX[i] = random.randint(0, 735)
			enemyY[i] = random.randint(50, 150)
		enemy(enemyX[i], enemyY[i], i)
		
	# bullet movement
	if bullet_state == "firing":
		fire_bullet(bulletX, bulletY)
		bulletY -= bullet_vel
	if bulletY+32 <= 0:
		bulletY=490
		bullet_state = "ready"

	show_score(scoreX, scoreY)
	player(playerX, playerY)
	pygame.display.update()
