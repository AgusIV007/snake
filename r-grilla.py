import pygame 

class Grilla:
	def __init__(self, width, height, screen, tamanoCelda) -> None:
		self.width = width
		self.height = height
		self.tamanoCelda = tamanoCelda
		self.screen = screen
		
		self.grid = [[0 for y in range(tamanoCelda)] for x in range(tamanoCelda)]
		self.tile_size = int((height * 0.8) / (self.tamanoCelda))
  
		self.renderGrid()

	def renderGrid(self):
		firstColor = (173, 215, 246)
		thirdColor = (101, 191, 255)
		tamanoFinal = int(self.height * 0.8)
		tile_size = int(tamanoFinal / self.tamanoCelda)

		grid_width = self.tamanoCelda * tile_size
		grid_height = self.tamanoCelda * tile_size

		offset_x = (self.width - grid_width) // 2
		offset_y = (self.height - grid_height) // 2

		for x in range(0, grid_width, tile_size):
			for y in range(0, grid_height, tile_size):
				rect = pygame.Rect(x + offset_x, y + offset_y, tile_size, tile_size)
				color = firstColor if (x // tile_size + y // tile_size) % 2 == 0 else thirdColor
				pygame.draw.rect(self.screen, color, rect.inflate(0, 0))
				
				indX, indY = x // tile_size, y // tile_size
				if self.grid[indX][indY] != 0:
					if self.grid[indX][indY] == 1:
						color = (0, 0, 255)  # Serpiente
						pygame.draw.rect(self.screen, color, rect.inflate(0, 0))
					elif self.grid[indX][indY] == 2:
				        # Dibuja un círculo rojo para la manzana
						pygame.draw.circle(self.screen, (255, 0, 0), rect.center, tile_size // 2)

					
	
	def obtenerPosicion(self, gridX, gridY):
		tamanoFinal = int(self.height * 0.8)  # Mantén la proporción de 0.8 para las celdas
		tile_size = int(tamanoFinal / self.tamanoCelda)

		# Calcula el tamaño total de la grilla
		grid_width = self.tamanoCelda * tile_size
		grid_height = self.tamanoCelda * tile_size

		# Calcula los offsets para centrar la grilla
		offset_x = (self.width - grid_width) // 2
		offset_y = (self.height - grid_height) // 2

		# Convierte las coordenadas de grilla (índices) a coordenadas en píxeles
		x = gridX * tile_size + offset_x
		y = gridY * tile_size + offset_y

		return x, y