import pygame
import random
import math

# Initializing the pygame.
pygame.init()

# Creating the game window.
screen = pygame.display.set_mode((800, 600))

# Changing the title of the game window.
pygame.display.set_caption("Space Invaders")

# Changing the logo of the game window.
logo = pygame.image.load("Logo.png")
pygame.display.set_icon(logo)

# Loading the background image for the game window.
bgImage = pygame.image.load("BackgroundImage.jpg")

# Loading background music.
pygame.mixer.music.load("BackgroundMusic.wav")
pygame.mixer.music.play(-1)

# Placing the player.
playerImage = pygame.image.load("Player.png")
playerX = 370
playerY = 480
playerXChange = 0

def displayPlayerImage(x, y):
	screen.blit(playerImage, (x, y))

# Placing the enemies.
enemyImage = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
numberOfEnemies = 10
for i in range(0, numberOfEnemies, 1):
	enemyImage.append(pygame.image.load("Enemy.png"))
	enemyX.append(random.randint(0, 736))
	enemyY.append(random.randint(0, 150))
	enemyXChange.append(1)
	enemyYChange.append(40)

def displayEnemyImage(x, y, i):
	screen.blit(enemyImage[i], (x, y))

# Placing the bullet.
bulletImage = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 2.5
bulletState = "ready"

def fireBullet(x, y):
	global bulletState
	bulletState = "fired"
	screen.blit(bulletImage, (x+16, y+10))

# Function to check for collision b/w the bullet and the enemy.
def collisionStatusBulletEnemy(bulletX, bulletY, enemyX, enemyY):
	distance = math.sqrt(math.pow(bulletX-enemyX,2)+math.pow(bulletY-enemyY,2))
	return distance <= 30

# To track the score.
scoreValue = 0
scoreFont = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10

def showScore(x, y):
	score = scoreFont.render("Score : "+str(scoreValue), True, (255, 255, 255))
	screen.blit(score, (x, y))

gameOverFont = pygame.font.Font("freesansbold.ttf", 64)

# Function for game over.
def gameOver():
	gameOverMessage = gameOverFont.render("Game Over", True, (255, 255, 255))
	screen.blit(gameOverMessage, (200, 250))

# Creating the game loop.
runningStatus = True
while runningStatus:

	# Changing the background color.
	screen.fill((0, 0, 0))

	# Changing the background image.
	screen.blit(bgImage, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			runningStatus = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerXChange = -1.5
			if event.key == pygame.K_RIGHT:
				playerXChange = 1.5
			if event.key == pygame.K_SPACE:
				if bulletState == "ready":
					# Generating the firing sound.
					firingSound = pygame.mixer.Sound("FiringSound.wav")
					firingSound.play()
					# Stores the current x-position of the player.
					bulletX = playerX
					fireBullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerXChange = 0

	displayPlayerImage(playerX, playerY)
	playerX += playerXChange
	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736

	for i in range(0, numberOfEnemies, 1):

		displayEnemyImage(enemyX[i], enemyY[i], i)

		# Checking for game over.
		if enemyY[i] > 440:
			for j in range(0, numberOfEnemies, 1):
				enemyY[j] = 2000
			gameOver()
			break

		if collisionStatusBulletEnemy(bulletX, bulletY, enemyX[i], enemyY[i]):
			# Generating the bullet-enemy collision sound.
			collisionBulletEnemySound = pygame.mixer.Sound("CollisionSound.wav")
			collisionBulletEnemySound.play()
			bulletY = 480
			bulletState = "ready"
			scoreValue += 1
			enemyX[i] = random.randint(0,736)
			enemyY[i] = random.randint(0,150)

		enemyX[i] += enemyXChange[i]
		if enemyX[i] <= 0:
			enemyXChange[i] = 1
			enemyY[i] += enemyYChange[i]
		elif enemyX[i] >= 736:
			enemyXChange[i] = -1
			enemyY[i] += enemyYChange[i]

	if bulletY <= 0:
		bulletState = "ready"
		bulletY = 480
	if bulletState == "fired":
		fireBullet(bulletX, bulletY)
		bulletY -= bulletYChange

	showScore(scoreX, scoreY)
	pygame.display.update()