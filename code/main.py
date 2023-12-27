import pygame, sys
from player import Player
from datetime import datetime
from gift import Gift, Extra
from random import choice, randint
from menu import Menu, GameOverScreen
 
current_time = datetime.now()

class Game:
	def __init__(self):
		# Player setup
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		#score setup
		self.score = 0
		
		
		self.font = pygame.font.Font('../font/Pixeled.ttf',20)
		self.blocks = pygame.sprite.Group()

		#Time
		self.start_time = pygame.time.get_ticks()
		
		
		# gift setup
		self.gift = pygame.sprite.Group()
		self.gift_setup(rows = 9, cols = 9)
		self.gift_direction = 1

		# Extra setup
		

		# Audio
		music = pygame.mixer.Sound('../audio/music.mp3')
		music.set_volume(0.2)
		music.play()
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

		self.extra_group = pygame.sprite.Group()
		self.extra = Extra(choice(['right', 'left']), screen_width)
		self.extra_group.add(self.extra)

	def gift_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: gift_sprite = Gift('yellow',x,y)
				elif row_index == 1: gift_sprite = Gift('green',x,y)
				elif row_index == 2: gift_sprite = Gift('blue',x,y)
				elif row_index == 3: gift_sprite = Gift('white',x,y)
				elif row_index == 4: gift_sprite = Gift('black',x,y)
				elif row_index == 5: gift_sprite = Gift('human',x,y)
				elif row_index == 6: gift_sprite = Gift('no',x,y)
				elif row_index == 6: gift_sprite = Gift('ring',x,y)

				else: gift_sprite = Gift('red',x,y)
				self.gift.add(gift_sprite)

	def gift_position_checker(self):
		all_gift = self.gift.sprites()
		for gift in all_gift:
			if gift.rect.right >= screen_width:
				self.gift_direction = -1
			elif gift.rect.left <= 0:
				self.gift_direction = 1

	def collision_checks(self):

		global game_over
		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
					

				# gift collisions
				gift_hit = pygame.sprite.spritecollide(laser,self.gift,True)
				if gift_hit:
					for gift in gift_hit:
						self.score += gift.value
					laser.kill()
					self.explosion_sound.play()

				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra_group,False):
					self.score -= 500
					laser.kill()




	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		screen.blit(score_surf,score_rect)

	#Time
	def countdown(self, seconds):
		global game_over
		elapsed_time = pygame.time.get_ticks() - self.start_time
		self.time = seconds * 1000 - elapsed_time
		if self.time <= 0:
			game_over = True
		time_surf = self.font.render(f'time: {str(int(self.time / 1000) + 1)}', False, 'white')
		time_rect = time_surf.get_rect(topleft = (650, -10))
		screen.blit(time_surf, time_rect)

		
	
	 #Score
	def score_end(self):
		score_surf = self.font.render(f'Your score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (200,200))
		screen.blit(score_surf,score_rect)

	def victory_message(self):
		if not self.gift.sprites():
			victory_surf = self.font.render('You won',False,'white')
			victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
			screen.blit(victory_surf,victory_rect)

	def run(self):
		self.player.update()
		self.gift.update(self.gift_direction)
		self.gift_position_checker()
		self.collision_checks()
		
		self.extra_group.update(screen_width)
		self.extra_group.draw(screen)

		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.blocks.draw(screen)
		self.gift.draw(screen)
		self.display_score()
		self.countdown(60)
		self.victory_message()
		if self.score <= 0:
			self.score = 0


if __name__ == '__main__':
	pygame.init()
	screen_width = 800
	screen_height = 800
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()
	
	menu = Menu(screen)
	selected_option = menu.run_menu()
	if selected_option == 0:  # Nếu người chơi chọn "Play"
		game = Game()
	if selected_option == 1:
		pygame.quit()
		sys.exit()

	game_over_screen = GameOverScreen()
	game_over = False
	background_end = pygame.image.load('../graphics/background.png').convert()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			

		if game_over:
			screen.blit(background, (0, 0))
			game_over_screen.draw(screen)
			replay_clicked = game_over_screen.handle_event(event)
			game.score_end()
			if replay_clicked:
				game = Game()
				game_over = False
		else:
			background = pygame.image.load("../graphics/background.png").convert()
			screen.blit(background, (0,0))
			game.run()
		
		pygame.display.flip()
		clock.tick(60)

