import pygame, sys
from player import Player
from datetime import datetime
from alien import Alien, Extra
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
		
		
		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 9, cols = 9)
		self.alien_direction = 1

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)

		# Audio
		music = pygame.mixer.Sound('../audio/music.mp3')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

	

	def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: alien_sprite = Alien('yellow',x,y)
				elif row_index == 1: alien_sprite = Alien('green',x,y)
				elif row_index == 2: alien_sprite = Alien('blue',x,y)
				elif row_index == 3: alien_sprite = Alien('white',x,y)
				elif row_index == 4: alien_sprite = Alien('black',x,y)
				else: alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)

	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= screen_width:
				self.alien_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= 0:
				self.alien_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	
	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),screen_width))
			self.extra_spawn_time = randint(400,800)

	def collision_checks(self):

		global game_over
		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
					

				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explosion_sound.play()

				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.score += 500
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
		if not self.aliens.sprites():
			victory_surf = self.font.render('You won',False,'white')
			victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
			screen.blit(victory_surf,victory_rect)

	def run(self):
		self.player.update()
		self.extra.update()
		self.aliens.update(self.alien_direction)
		self.alien_position_checker()
		self.extra_alien_timer()
		self.collision_checks()
		
		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.extra.draw(screen)
		self.display_score()
		self.countdown(60)
		self.victory_message()


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
	background = pygame.image.load('../graphics/background.png').convert()

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

