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
        self.direccion = (0, 0)

    def generar_manzana(self):
        while True:
            x = random.randint(0, self.tamano - 1)
            y = random.randint(0, self.tamano - 1)
            if (x, y) not in self.posicion_serpiente:
                return (x, y)
    
    def obtener_izquierda(self):
        if self.direccion == (0, -1):
            return (-1, 0)
        elif self.direccion == (0, 1):
            return (1, 0)
        elif self.direccion == (-1, 0):
            return (0, 1)
        elif self.direccion == (1, 0):
            return (0, -1)

    def obtener_direccion_opuesta(self, direccion):
        nuevaDireccion = (direccion[0] * -1, direccion[1] * -1) 
        return nuevaDireccion

    def step(self, accion):
        assert accion in {0,1,2}, "Accion invalida"
        recompensa = 0
        termino = False
        if self.direccion == (0, 0):
            self.direccion = (-1, 0)
        if accion == 1:
            self.direccion = self.obtener_izquierda()
        elif accion == 2:
            self.direccion = self.obtener_direccion_opuesta(self.obtener_izquierda())
        cabeza_x, cabeza_y = self.posicion_serpiente[0]
        nueva_cabeza = (cabeza_x + self.direccion[0], cabeza_y + self.direccion[1])
        if (nueva_cabeza in self.posicion_serpiente or 
            nueva_cabeza[0] < 0 or nueva_cabeza[0] >= self.tamano or 
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= self.tamano):
            termino = True
            recompensa = -1
            self.reset()
            return self.obtener_estado(termino), recompensa, termino
        if nueva_cabeza == self.posicion_manzana:
            self.longitud += 1 
            self.posicion_manzana = self.generar_manzana()  
            self.posicion_serpiente.insert(0, nueva_cabeza)
            recompensa = 1     
        else:
            self.posicion_serpiente.insert(0, nueva_cabeza)
            self.posicion_serpiente.pop()
        return self.obtener_estado(termino), recompensa, termino

    def render(self, ventana):
        for segmento in self.posicion_serpiente:
            x, y = segmento
            pygame.draw.rect(ventana, (72, 118, 237), (x * 40, y * 40, 40, 40))

        manzana_x, manzana_y = self.posicion_manzana
        pygame.draw.rect(ventana, (255, 0, 0), (manzana_x * 40, manzana_y * 40, 40, 40)) 
    
    def obtener_estado(self, termino):
        muerte0 = 0
        muerte1 = 0
        muerte2 = 0
        
        if not termino:
            muerte0 = self.obtener_muerte(self.direccion)
            muerte1 = self.obtener_muerte(self.obtener_izquierda())
            muerte2 = self.obtener_muerte(self.obtener_direccion_opuesta(self.obtener_izquierda()))

        direccionArr = self.obtener_direccion((0, -1))
        direccionAb = self.obtener_direccion((0, 1))
        direccionIz = self.obtener_direccion((-1, 0))
        direccionDer = self.obtener_direccion((1, 0))

        manzanaArr = 0
        manzanaAb = 0
        manzanaIz = 0
        manzanaDer = 0

        if self.posicion_manzana[1] < self.posicion_serpiente[0][1]:
            manzanaArr = 1
        elif self.posicion_manzana[1] > self.posicion_serpiente[0][1]:
            manzanaAb = 1
        if self.posicion_manzana[0] < self.posicion_serpiente[0][0]:
            manzanaIz = 1
        elif self.posicion_manzana[0] > self.posicion_serpiente[0][0]:
            manzanaDer = 1

        return muerte1, muerte2, muerte0, direccionArr, direccionDer, direccionAb, direccionIz, manzanaArr, manzanaIz, manzanaDer, manzanaAb

    def obtener_muerte(self, direccion):
        cabeza_x, cabeza_y = self.posicion_serpiente[0]
        nueva_cabeza = (cabeza_x + direccion[0], cabeza_y + direccion[1])
        if (nueva_cabeza in self.posicion_serpiente or 
            nueva_cabeza[0] < 0 or nueva_cabeza[0] >= self.tamano or 
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= self.tamano):
            return 1
        return 0

    def obtener_direccion(self, direccion):
        if self.direccion == direccion:
            return 1
        return 0
    
class Ventana:
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((640, 640))
        pygame.display.set_caption('Snake')
        self.cuadricula_tamano = 40

    def dibujar_cuadricula(self):
        for x in range(0, 640, self.cuadricula_tamano):
            for y in range(0, 640, self.cuadricula_tamano):
                color = (170, 215, 81) if (x // self.cuadricula_tamano + y // self.cuadricula_tamano) % 2 == 0 else (162, 209, 73)
                pygame.draw.rect(self.ventana, color, (x, y, self.cuadricula_tamano, self.cuadricula_tamano))

    def ejecutar(self, juego):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.ventana.fill((0, 0, 0))
            
            self.dibujar_cuadricula()
            
            juego.render(self.ventana)
            
            pygame.display.flip()