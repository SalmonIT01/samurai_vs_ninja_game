import pygame

class Fighter():
	def __init__(self,player,x,y,flip,data,sprite_sheet,animation_step,sound,sound2):

	   self.size = data[0]
	   self.player = player
	   self.img_scale = data[1]
	   self.offset = data[2]
	   self.flip = flip
	   self.animation_list = self.load_img(sprite_sheet,animation_step)
	   self.action = 0   #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
	   self.frame_index = 0
	   self.img = self.animation_list[self.action][self.frame_index]
	   self.update_time = pygame.time.get_ticks()
	   self.rect = pygame.Rect(x,y,80,180)
	   self.vel_y = 0
	   self.run = False
	   self.jump = False
	   self.attacking = False
	   self.attack_type = 0
	   self.health = 100
	   self.attack_sound = sound
	   self.attack_sound2 = sound2
	   self.attack_cooldown = 0
	   self.takehit = False
	   self.alive = True


	def load_img(self,sprite_sheet,animation_step):
		
		animation_list = []
		for y,animation in enumerate(animation_step):
			temp_img_list = []
			for x in range(animation):
				temp_img = sprite_sheet.subsurface(x*self.size,y*self.size,self.size , self.size)
				temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.img_scale, self.size * self.img_scale)))
			animation_list.append(temp_img_list)
		return animation_list

	def move(self,screen_width,screen_height,target,round_over):
		speed = 10
		gravity = 1.5
		dx = 0
		dy = 0
		self.run =False
		self.attack_type = 0

		#key presses
		key = pygame.key.get_pressed()
        #can only perform other actions if not currently attacking
		if self.attacking == False and self.alive == True and round_over == False:
			#player 1 control
			if self.player == 1:#movement
				if key[pygame.K_a]:
					dx = -speed
					self.run = True

				if key[pygame.K_d]:
					dx = speed
					self.run = True
				#jump
				if key[pygame.K_w ] and self.jump == False:
					self.vel_y = -35
					self.jump = True
				#attack
				if key[pygame.K_j] :
					self.attack(target)
					self.attack_type = 1
					
						
				if key[pygame.K_k]:
					self.attack2(target)
					self.attack_type = 2

			#player 2 control
			if self.player == 2:
			    #movement
				if key[pygame.K_LEFT]:
					dx = -speed
					self.run = True

				if key[pygame.K_RIGHT]:
					dx = speed
					self.run = True
				#jump
				if key[pygame.K_UP ] and self.jump == False:
					self.vel_y = -25
					self.jump = True
					#attack
				if key[pygame.K_KP1]:
					self.attack(target)
					self.attack_type = 1
					
				if key[pygame.K_KP2]:
					self.attack2(target)
					self.attack_type = 2

		#add gravity
		self.vel_y += gravity
		dy += self.vel_y
	    
	    #ensure player stays on screen
		if self.rect.left + dx < 0:
			dx = -self.rect.left
		if self.rect.right + dx > screen_width:
			dx = screen_width - self.rect.right
		if self.rect.bottom + dy > screen_height - 110:
			self.vel_y = 0
			self.jump = False
			dy = screen_height - 110 - self.rect.bottom
		#ensure players face each other
		if target.rect.centerx > self.rect.centerx:
			self.flip = False
		else:
			self.flip = True	
		#add atk cooldown
		if self.attack_cooldown > 0:
			self.attack_cooldown -=1	
		
		#update player position
		self.rect.x += dx
		self.rect.y += dy
	
	def update(self):
		#fighter death
		if self.health <= 0:
			self.alive = False
			self.health = 0
			self.update_action(6)
		#when fighter take damage
		elif self.takehit == True:
			self.update_action(5)
		#run
		elif self.attacking == True:
			if self.attack_type == 1:
				self.update_action(3)
			elif self.attack_type==2:
				self.update_action(4)

		elif self.jump == True:
			self.update_action(2)
		#run
		elif self.run == True:
			self.update_action(1)
		else:
			self.update_action(0)

		
		animation_cooldown = 70
		self.img = self.animation_list[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.frame_index += 1
			self.update_time = pygame.time.get_ticks()
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.alive == False:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0
			if self.player == 1:
				if self.action == 3:
					self.attacking = False
					self.attack_cooldown = 10
				
				if self.action == 4:
					self.attacking = False
					self.attack_cooldown = 100

				if self.action == 5:
					self.takehit = False
					self.attacking = False
					self.attack_cooldown = 10

			if self.player == 2:
				if self.action == 3 :
					self.attacking = False
					self.attack_cooldown = 20
				if self.action == 4:
					self.attacking = False
					self.attack_cooldown = 200
				if self.action == 5:
					self.takehit = False
					self.attacking = False
					self.attack_cooldown = 10

	def attack(self,target):
		if self.player == 1:
			if self.attack_cooldown == 0:
				self.attacking = True
				self.attack_sound.play()
				attacking_rect = pygame.Rect(self.rect.centerx-(2*self.rect.width*self.flip),self.rect.y,2*self.rect.width,self.rect.height)
				if attacking_rect.colliderect(target.rect):
					
						self.attack_sound2.play()
						target.health -= 10
						target.takehit = True


		if self.player == 2:
			if self.attack_cooldown == 0:
				self.attacking = True
				self.attack_sound.play()
				attacking_rect = pygame.Rect(self.rect.centerx-(4*self.rect.width*self.flip),self.rect.y,4*self.rect.width,self.rect.height)
				if attacking_rect.colliderect(target.rect):
					self.attack_sound2.play()
					target.health -= 12
					target.takehit = True
	
	def attack2(self,target):
		if self.player == 1:
			if self.attack_cooldown == 0:
				self.attacking = True
				self.attack_sound.play()
				attacking_rect = pygame.Rect(self.rect.centerx-(2*self.rect.width*self.flip),self.rect.y,2*self.rect.width,self.rect.height)
				if attacking_rect.colliderect(target.rect):
					self.attack_sound2.play()
					target.health -= 20
					target.takehit = True

		if self.player == 2:
			if self.attack_cooldown == 0:
				self.attacking = True
				self.attack_sound.play()
				attacking_rect = pygame.Rect(self.rect.centerx-(4*self.rect.width*self.flip),self.rect.y,4*self.rect.width,self.rect.height)
				if attacking_rect.colliderect(target.rect):
					self.attack_sound2.play()
					target.health -= 25
					target.takehit = True
			

	def update_action(self, new_action):
		if new_action != self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()


	def draw(self,surface):
		img = pygame.transform.flip(self.img, self.flip, False)
		
		surface.blit(img,(self.rect.x - (self.offset[0] * self.img_scale), self.rect.y - (self.offset[1] * self.img_scale)))
