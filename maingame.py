import pygame
from pygame import mixer
from player import Fighter
mixer.init()
pygame.init()
ScreenH = 600
ScreenW = 1000
#พี่ไม่เชื่อ

screen = pygame.display.set_mode((ScreenW,ScreenH))
pygame.display.set_caption("Samurai VS Ninja!")


#set framerate
clock = pygame.time.Clock()
FPS = 60

#define color
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0, 0, 255)
#load vicory image
victory_img = pygame.image.load("assets1/img/bg/icon.png").convert_alpha()
p1win = pygame.image.load('assets1/img/bg/player1win.png').convert_alpha()
p2win = pygame.image.load('assets1/img/bg/player2win.png').convert_alpha()
#icon game
icon = pygame.image.load('assets1/img/bg/katana.png')
pygame.display.set_icon(icon)

#define game var
intro_count = 4
last_count_update = pygame.time.get_ticks()
player1_score = 0
player2_score = 0
ROUND = 1
round_over = False
roundover_cooldown = 3000

#define swordman
Ninja_size = 162
Ninja_scale = 4
Ninja_offset = [72,55]
Ninja_data = [Ninja_size,Ninja_scale,Ninja_offset]

Samurai_size = 162
Samurai_scale = 4.3
Samurai_offset = [72,59]
Samurai_data = [Samurai_size,Samurai_scale,Samurai_offset]

#load music and sounds
pygame.mixer.music.load("assets1/audio/music3.mp3")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("assets1/audio/swordwind.mp3")
sword_fx.set_volume(0.75)
knife_fx = pygame.mixer.Sound('assets1/audio/sword.mp3')
knife_fx.set_volume(0.75)
katana_fx = pygame.mixer.Sound("assets1/audio/katana.mp3")
katana_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets1/img/bg/newbg.jpg").convert_alpha()#
#load spritesheet
#define font
count_font = pygame.font.Font("assets1/font/japan.otf", 70)
score_font = pygame.font.Font("assets1/font/japan.otf", 35)
round_font = pygame.font.Font("assets1/font/japan.otf",40)

ninja_sheet = pygame.image.load("assets1/img/ninja/Sprites/ninja1.png").convert_alpha()
samurai_sheet = pygame.image.load("assets1/img/samurai/Sprites/samurai.png").convert_alpha()

#define number of steps in each animation
Ninja_animation_step = [4,7,1,4,4,3,6]
Samurai_animation_step = [7,8,1,4,5,4,6]


#function for drawing text
def draw_text(text, font, text_color, x, y):
  img = font.render(text, True, text_color)
  screen.blit(img, (x, y))
#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (ScreenW, ScreenH))
  screen.blit(scaled_bg, (0, 0))
#health bar
def draw_health_bar(health,x,y):
	ratio = health/100
	pygame.draw.rect(screen,BLACK,(x-2,y-2,404,34))
	pygame.draw.rect(screen,RED,(x,y,400,30))
	pygame.draw.rect(screen,GREEN,(x,y,400*ratio,30))


#create 2 player
Fighter_1 = Fighter(1,200,310,False,Ninja_data,ninja_sheet,Ninja_animation_step,sword_fx,knife_fx)
Fighter_2 = Fighter(2,700,310,True,Samurai_data,samurai_sheet,Samurai_animation_step,sword_fx,katana_fx)



  
run = True
while run:
	draw_bg()

	#show player health bar
	draw_health_bar(Fighter_1.health,20,20)
	draw_health_bar(Fighter_2.health,580,20)
	draw_text("P1: " + str(player1_score), score_font, BLUE, 20, 60)
	draw_text("P2: " + str(player2_score), score_font, RED, 900, 60)
	draw_text("ROUND:" +str(ROUND),round_font,YELLOW,420,50)

	clock.tick(FPS)
	#update time countdown

	
	if intro_count <=0:
		Fighter_1.move(ScreenW,ScreenH,Fighter_2,round_over)
		Fighter_2.move(ScreenW,ScreenH,Fighter_1,round_over)
	else:
		draw_text(str(intro_count), count_font, RED, ScreenW / 2, ScreenH / 3)
		if (pygame.time.get_ticks() - last_count_update) >= 1000:
			intro_count -= 1
			last_count_update = pygame.time.get_ticks()

			
 
	
	#update fighter
	Fighter_1.update()
	Fighter_2.update()
  
  #show characters on screen
	Fighter_1.draw(screen)
	Fighter_2.draw(screen)
	#player defeat
	
	if round_over == False:
		if Fighter_1.alive == False:
			player2_score += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()

			

		if Fighter_2.alive == False:
			player1_score += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()



	elif player1_score == 2 and player2_score == 0 :
		screen.blit(p1win,(100,100))
		round_over = True
	elif player1_score == 0 and player2_score == 2 :
		

		screen.blit(p2win,(420,100))
		round_over = True
		
	elif player1_score == 2 and player2_score == 1 :
		screen.blit(p1win,(100,100))
		round_over = True
	elif player1_score == 1 and player2_score == 2 :
		screen.blit(p2win,(420,100))
		round_over = True  


	elif round_over == True:
		
		screen.blit(victory_img,(360,100))
		
		if pygame.time.get_ticks() - round_over_time > roundover_cooldown:
			ROUND += 1
			round_over = False
			intro_count = 4
			Fighter_1 = Fighter(1,200,310,False,Ninja_data,ninja_sheet,Ninja_animation_step,sword_fx,knife_fx)
			Fighter_2 = Fighter(2,700,310,True,Samurai_data,samurai_sheet,Samurai_animation_step,sword_fx,katana_fx)





	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()