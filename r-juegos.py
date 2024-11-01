# En este archivo tenemos la clase que representa el juego a programar, es importante que siga la interfaz que tiene esta clase, o sea que tenga las funciones que hay en este archivo.

import pygame
from grilla import Grilla
import random
import time
import sys

class Snake():
	def __init__(self, tamanoCelda, maxManzanas):
		self.corriendo = True
		self.sigueVivo = True
		self.tamanoCelda = tamanoCelda
		self.direction = (0, -1)  # Oeste = (-1, 0), Este = (1, 0), Norte = (0, -1), Sur = (0, 1)
		self.snake_length = 1
		self.manzanas = 0
		self.maximoManzanas = maxManzanas
		self.applePosition = None

		### Completar
		pygame.init()
		self.width, self.height = 800, 600

		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Snake Game")
		self.grilla = Grilla(self.width, self.height, self.screen, self.tamanoCelda)
		
		self.reset()
		self.render()

	def initSnake(self):
		self.direccion = random.randint(0, 2) # (0 = sigue derecho, 1 = dobla a la izquierda, 2 = dobla a la derecha)
		self.snake_length = 1
		randomX, randomY = random.randint(self.tamanoCelda - (self.tamanoCelda - 1), self.tamanoCelda - 1), random.randint(self.tamanoCelda - (self.tamanoCelda - 1), self.tamanoCelda - 1)
		self.grilla.grid = [[0 for y in range(self.tamanoCelda)] for x in range(self.tamanoCelda)]
		self.grilla.grid[randomX][randomY] = 1
		self.snake_head = (randomX, randomY)
		self.snake = [(randomX, randomY)]
		

	def generarApple(self):
		empty_cells = [(row, col) for row in range(len(self.grilla.grid)) for col in range(len(self.grilla.grid[row])) if self.grilla.grid[row][col] == 0]
		if empty_cells:
			while self.manzanas < self.maximoManzanas:
				apple_position = random.choice(empty_cells)
				self.applePosition = (apple_position[0], apple_position[1])
				self.grilla.grid[apple_position[0]][apple_position[1]] = 2
				self.manzanas += 1

	# Reinicia el juego:
	#   - Pone la longitud de la serpiente en 1.
	#   - Coloca la serpiente en un lugar random.
	#   - Pone la fruta en una posicion random
	def reset(self):
		self.game_over = False  # Reiniciar estado del juego
		self.sigueVivo = True
		self.hayManzana = False
		self.manzanas = 0
		self.initSnake()
		return self.abstraccionGrilla(0, self.snake_head, True)

	# Mueve al jugador una vez, en fuincion a la accion realizada.
	# Devuelve 3 cosas:
	#   - El nuevo estado del juego
	#   - Si el juego termino o no (o sea si la serpiente murio o no)
	#   - La recompenza de la accion realizada (0 si no pasa nada, 1 si agarro una fruta, -1 si perdio)
	# Recordatorio: un estado es una lista de 11 numeros bienarios (1 o 0), cada uno de estos bits indican si se cumple una condicion o no (estas 11 condiciones estan detalladas en el informe).
	def step(self, accion):
		assert accion in {0,1,2}, "Accion invalida"     # Chequea que la accion sea valida (0 = sigue derecho, 1 = dobla a la izquierda, 2 = dobla a la derecha)
		print("--------------------------------------------------\n")
		time.sleep(1)
		self.generarApple()
		recompensa = None
		if accion == 1:  # Turn left
			self.direction = (-self.direction[1], self.direction[0])
		elif accion == 2:  # Turn right
			self.direction = (self.direction[1], -self.direction[0])
		print(self.direction)	
		# Calculate new head position
		new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
		self.snake_head = new_head
		# Check for collision with walls or itself
		if ((new_head[0] < 0) or (new_head[0] >= len(self.grilla.grid)) or (new_head[1] < 0) or (new_head[1] >= len(self.grilla.grid[0])) or (self.grilla.grid[new_head[0]][new_head[1]] == 1)):
			return self.abstraccionGrilla(accion, new_head, False), False, -1

		# Check for apple
		if self.grilla.grid[new_head[0]][new_head[1]] == 2:
			recompensa = 1
			self.manzanas -= 1
			self.snake.insert(0, new_head)  # Grow snake
		else:
			recompensa = 0
			self.snake.insert(0, new_head)
			tail = self.snake.pop()
			self.grilla.grid[tail[0]][tail[1]] = 0  # Remove tail from grid

		# Update grid with new head position
		self.grilla.grid[new_head[0]][new_head[1]] = 1

		self.render()
		return self.abstraccionGrilla(accion, new_head, True), True, recompensa


	# Actualiza la informacion que se muestra en pantalla usando pygame.
	def render(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		secondColor = (3, 53, 74)

		self.screen.fill(secondColor)
		self.grilla.renderGrid()
		pygame.display.flip()

	## 
	def abstraccionGrilla(self, accion, new_head, jugando):
		izqMuere = 0
		derMuere = 0
		adeMuere = 0
		if (not jugando):
			if accion == 0:  # adelante
				adeMuere = 1 if ((new_head[0] < 0) or (new_head[0] >= len(self.grilla.grid)) or (new_head[1] < 0) or (new_head[1] >= len(self.grilla.grid[0])) or (self.grilla.grid[new_head[0]][new_head[1]] == 1)) else 0
			elif accion == 1:  # izquierda
				izqMuere = 1 if ((new_head[0] < 0) or (new_head[0] >= len(self.grilla.grid)) or (new_head[1] < 0) or (new_head[1] >= len(self.grilla.grid[0])) or (self.grilla.grid[new_head[0]][new_head[1]] == 1)) else 0
			elif accion == 2:  # derecha
				derMuere = 1 if ((new_head[0] < 0) or (new_head[0] >= len(self.grilla.grid)) or (new_head[1] < 0) or (new_head[1] >= len(self.grilla.grid[0])) or (self.grilla.grid[new_head[0]][new_head[1]] == 1)) else 0

		dirNorte = 1 if self.direction == (0,-1) else 0
		dirSur = 1 if self.direction == (0,1) else 0
		dirOeste = 1 if self.direction == (-1,0) else 0
		dirEste = 1 if self.direction == (1,0) else 0
		manzanaIzquierda = 0
		manzanaDerecha = 0
		manzanaArriba = 0
		manzanaAbajo = 0
		if self.applePosition:
			manzanaIzquierda = 1 if self.applePosition[0] < self.snake_head[0] else 0
			manzanaDerecha = 1 if self.applePosition[0] > self.snake_head[0] else 0
			manzanaArriba = 1 if self.applePosition[1] < self.snake_head[1] else 0
			manzanaAbajo = 1 if self.applePosition[1] > self.snake_head[1] else 0
		return (izqMuere, derMuere, adeMuere, dirNorte, dirSur, dirOeste, dirEste, manzanaIzquierda, manzanaDerecha, manzanaArriba, manzanaAbajo)