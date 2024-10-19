# En este archivo tenemos las clases que representan jugadores
import pickle
import random
import pygame

class Random():
    def __init__(self, juego):
        self.juego = juego
    
    def jugar(self):
        while True:
            direccion_actual1 = self.juego.direccion[0]
            direccion_actual2 = self.juego.direccion[1]
            direccion_actual_opuesta = self.obtenerDireccionOpuesta(direccion_actual1, direccion_actual2)
            direcion_nueva = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)]) # Abajo, Derecha, Arriba, Izquierda
            while True:
                if (direccion_actual_opuesta != direcion_nueva):
                    self.juego.direccion = direcion_nueva
                    break
                direcion_nueva = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)]) 
            self.juego.direccion = direcion_nueva 
            self.juego.step()
            if self.juego.longitud <= 0:
                break
            pygame.time.delay(150)

    def obtenerDireccionOpuesta(self, direccion_actual1, direccion_actual2):
        nuevaDireccion = (direccion_actual1 * -1, direccion_actual2 * -1) 
        return nuevaDireccion

class IA():
    def __init__(self, juego):
        self.juego = juego
        self.path = None
        self.Q = {}
        self.alpha = 0.1  # Tasa de aprendizaje
        self.gamma = 0.9  # Factor de descuento
        self.epsilon = 0.1  # Tasa de exploración
        self.episodios = 1000  # Número de episodios para entrenar

    def set_path(self, path):
        self.path = path

    def jugar(self):
        estado = self.obtener_estado()
        while True:
            if random.random() < self.epsilon:
                # Exploración: elige un movimiento aleatorio
                accion = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            else:
                # Explotación: elige el mejor movimiento conocido
                acciones = self.Q.get(estado, {})
                accion = max(acciones, key=acciones.get, default=(0, 1))

            self.juego.direccion = accion
            self.juego.step()

            # Actualiza el estado y la recompensa
            nuevo_estado = self.obtener_estado()
            recompensa = self.calcular_recompensa()

            # Actualizar la tabla Q
            self.Q.setdefault(estado, {})
            self.Q[estado][accion] = self.Q[estado].get(accion, 0) + self.alpha * (recompensa + self.gamma * max(self.Q.get(nuevo_estado, {}).values(), default=0) - self.Q[estado][accion])

            estado = nuevo_estado

    def entrenar(self):
        for episodio in range(self.episodios):
            self.juego.reset()
            estado = self.obtener_estado()
            while True:
                if random.random() < self.epsilon:
                    # Exploración: elige un movimiento aleatorio
                    accion = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                else:
                    # Explotación: elige el mejor movimiento conocido
                    acciones = self.Q.get(estado, {})
                    accion = max(acciones, key=acciones.get, default=(0, 1))

                self.juego.direccion = accion
                self.juego.step()

                nuevo_estado = self.obtener_estado()
                recompensa = self.calcular_recompensa()

                # Actualizar la tabla Q
                self.Q.setdefault(estado, {})
                self.Q[estado][accion] = self.Q[estado].get(accion, 0) + self.alpha * (recompensa + self.gamma * max(self.Q.get(nuevo_estado, {}).values(), default=0) - self.Q[estado][accion])

                estado = nuevo_estado

                # Terminar el episodio si el juego ha terminado (puedes ajustar la condición)
                if self.juego.longitud <= 0:
                    break

    def obtener_estado(self):
        # Devuelve una representación del estado actual del juego
        # Aquí puedes incluir la posición de la serpiente y la posición de la comida
        posicion = self.juego.posicion_serpiente[0]  # La cabeza de la serpiente
        return (posicion, tuple(self.juego.posicion_serpiente), self.juego.direccion)

    def calcular_recompensa(self):
        # Aquí defines la lógica para calcular la recompensa
        if self.juego.longitud > len(self.juego.posicion_serpiente):
            return 1  # Comer
        elif self.juego.posicion_serpiente[0] in self.juego.posicion_serpiente[1:] or \
             self.juego.posicion_serpiente[0][0] < 0 or self.juego.posicion_serpiente[0][0] >= self.juego.tamano or \
             self.juego.posicion_serpiente[0][1] < 0 or self.juego.posicion_serpiente[0][1] >= self.juego.tamano:
            return -1  # Chocar
        return 0  # Otra situación

    def save(self):
        if self.path is not None:
            with open(self.path, 'wb') as f:
                pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        if self.path is not None:
            with open(self.path, 'rb') as f:
                self.Q = pickle.load(f)