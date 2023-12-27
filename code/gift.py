import pygame

class Gift(pygame.sprite.Sprite):
	def __init__(self,name,x,y):
		super().__init__()
		file_path = '../graphics/' + name + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

		if name == 'red': self.value = 100
		elif name == 'green': self.value = 200
		else: self.value = 300

	def update(self,direction):
		self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('../graphics/extra.png').convert_alpha()
        
        if side == 'right':
            self.rect = self.image.get_rect(topleft=(screen_width + 50, 600))
            self.direction = -1  # Ban đầu di chuyển sang trái
        else:
            self.rect = self.image.get_rect(topleft=(-50, 600))
            self.direction = 1  # Ban đầu di chuyển sang phải

        self.speed = 7

    def update(self, screen_width):
        self.rect.x += self.speed * self.direction

        # Kiểm tra nếu chạm vào biên trái hoặc biên phải thì đổi hướng di chuyển
        if self.rect.left <= 0:
            self.direction = 1  # Đổi hướng sang phải
        elif self.rect.right >= screen_width:
            self.direction = -1  # Đổi hướng sang trái
