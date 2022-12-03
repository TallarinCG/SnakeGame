import pygame
from pygame.math import Vector2 
import random
import os

pygame.init()

width = 720
height = 480

win = pygame.display.set_mode((width, height))

snake_body = pygame.transform.scale(pygame.image.load(os.path.join(r"/home/alonso/Documentos/Python/Juego/snakebody.png")),(20,20))
snake_head = []
for x in range(1,5):
	snake_head+=[pygame.transform.scale(pygame.image.load(os.path.join(r"/home/alonso/Documentos/Python/Juego/SnakeHead"+str(x)+".png")),(20,20))]
apple = pygame.transform.scale(pygame.image.load(os.path.join(r"/home/alonso/Documentos/Python/Juego/manzana.png")),(20,20))

eat_sound = pygame.mixer.Sound("coin.wav")


score_text = pygame.font.SysFont("Russo One",15)

class Snake:
	def __init__(self):
		self.body = [Vector2(20,100),Vector2(20,110),Vector2(20,120)]
		self.direction = Vector2(0,-20)
		self.add = False

	def draw(self):
		for bloque in self.body:
			win.blit(snake_body,(bloque.x,bloque.y))

		if self.direction == Vector2(0,-20):
			win.blit(snake_head[0],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(0,20):
			win.blit(snake_head[2],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(20,0):
			win.blit(snake_head[1],(self.body[0].x,self.body[0].y))

		if self.direction == Vector2(-20,0):
			win.blit(snake_head[3],(self.body[0].x,self.body[0].y))

	def move(self):
		
		#[0,1,2] --> [0,1] --> [None,0,1] --> [-1,0,1]
		if self.add == True:
			body_copy = self.body
			body_copy.insert(0,body_copy[0]+self.direction)
			self.body = body_copy[:]
			self.add = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0]+self.direction)
			self.body = body_copy[:]


	def move_up(self):
		self.direction = Vector2(0,-20)

	def move_down(self):
		self.direction = Vector2(0,20)

	def move_right(self):
		self.direction = Vector2(20,0)

	def move_left(self):
		self.direction = Vector2(-20,0)

	def die(self):
		if self.body[0].x >= width+20 or self.body[0].y >= height+20 or self.body[0].x <= -20 or self.body[0].y <= -20:
			return True

		#SNake se toca a si misma
		for i in self.body[1:]:
			if self.body[0] == i:
				return True

class Apple:
	def __init__(self):
		self.generate()


	def draw(self):
		win.blit(apple,(self.pos.x,self.pos.y))


	def generate(self):
		self.x = random.randrange(0,width/20)
		self.y = random.randrange(0,height/20)
		self.pos = Vector2(self.x*20,self.y*20)

	def check_collision(self,snake):

		if snake.body[0] == self.pos:
			self.generate()
			snake.add = True

			return True

		for bloque in snake.body[1:]:
			if self.pos == bloque:
				self.generate()

		return False


def main():

	snake = Snake()
	apple = Apple()
	score = 0

	fps = pygame.time.Clock()

	while True:

		fps.tick(10)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN and snake.direction.y != 20:
				if event.key == pygame.K_UP:
					snake.move_up()

			if event.type == pygame.KEYDOWN and snake.direction.y != -20:
				if event.key == pygame.K_DOWN:
					snake.move_down()


			if event.type == pygame.KEYDOWN and snake.direction.x != -20:
				if event.key == pygame.K_RIGHT:
					snake.move_right()

			if event.type == pygame.KEYDOWN and snake.direction.x != 20:
				if event.key == pygame.K_LEFT:
					snake.move_left()

						
		win.fill((175,215,70))
		snake.draw()
		apple.draw()

		snake.move()


		if apple.check_collision(snake):
			score+=1
			eat_sound.play()

		snake.die()
		if snake.die():
			quit()


		text = score_text.render("Score: {}".format(score),1,(255,255,255))
		win.blit(text,(width-text.get_width()-20,20))

		pygame.display.update()

main()      