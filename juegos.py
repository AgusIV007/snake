# En este archivo tenemos la clase que representa el juego a programar, es importante que siga la interfaz que tiene esta clase, o sea que tenga las funciones que hay en este archivo.
import pygame 
import sys
import random

class Snake():
    def __init__(self, tamano):
        self.tamano = tamano
        self.reset()
        self.posicion_manzana = self.generar_manzana()
        
    def reset(self):
        self.longitud = 1
        self.posicion_serpiente = [(self.tamano // 2, self.tamano // 2)]
        self.direccion = (0, 0)  # Inicialmente no se mueve

    def generar_manzana(self):
        while True:
            x = random.randint(0, self.tamano - 1)
            y = random.randint(0, self.tamano - 1)
            if (x, y) not in self.posicion_serpiente:
                return (x, y)

    def step(self):
        # Mueve la serpiente en la dirección actual
        cabeza_x, cabeza_y = self.posicion_serpiente[0]
        nueva_cabeza = (cabeza_x + self.direccion[0], cabeza_y + self.direccion[1])

        # Verificar colisiones
        if (nueva_cabeza in self.posicion_serpiente or 
            nueva_cabeza[0] < 0 or nueva_cabeza[0] >= self.tamano or 
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= self.tamano):
            self.longitud = 0  # Terminar el juego si hay colisión
            return

        # Comprobar si se ha comido la manzana
        if nueva_cabeza == self.posicion_manzana:
            self.longitud += 1  # Aumentar longitud
            self.posicion_manzana = self.generar_manzana()  # Generar nueva manzana
            self.posicion_serpiente.insert(0, nueva_cabeza)  
        else:
            # Agregar nueva cabeza y eliminar la cola
            self.posicion_serpiente.insert(0, nueva_cabeza)
            self.posicion_serpiente.pop()  # Eliminar la cola

    def render(self, ventana):
        for segmento in self.posicion_serpiente:
            x, y = segmento
            pygame.draw.rect(ventana, (0, 255, 0), (x * 40, y * 40, 40, 40))  # Dibuja la serpiente

        # Dibuja la manzana
        manzana_x, manzana_y = self.posicion_manzana
        pygame.draw.rect(ventana, (255, 0, 0), (manzana_x * 40, manzana_y * 40, 40, 40))  # Dibuja la manzana


class Ventana:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((640, 640))
        pygame.display.set_caption('Snake')
        self.cuadricula_tamano = 40

    def dibujar_cuadricula(self):
        for x in range(0, 640, self.cuadricula_tamano):
            for y in range(0, 640, self.cuadricula_tamano):
                color = (255, 255, 255) if (x // self.cuadricula_tamano + y // self.cuadricula_tamano) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(self.ventana, color, (x, y, self.cuadricula_tamano, self.cuadricula_tamano))

    def ejecutar(self, juego):  # Asegúrate de que el método acepte el argumento juego
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Limpiar pantalla
            self.ventana.fill((0, 0, 0))
            
            # Dibujar la cuadrícula
            self.dibujar_cuadricula()
            
            # Dibujar la serpiente
            juego.render(self.ventana)
            
            # Actualizar la pantalla
            pygame.display.flip()