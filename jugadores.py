# En este archivo tenemos las clases que representan jugadores
import pickle
import random
import pygame

# class Random():
#     def __init__(self, juego):
#         self.juego = juego

#     def jugar(self):
#         while True:
#             accion = random.choice([0, 1, 2])  # Generar acción aleatoria
#             estado, recompensa, termino = self.juego.step(accion)
#             if termino:
#                 break
#             pygame.time.delay(150)

class Random():
    def __init__(self, juego):
        self.juego = juego
    
    def jugar(self):
        print("hah")
        while True:
            direcion_nueva = random.choice([0, 1, 2])
            step = self.juego.step(direcion_nueva)
            print(step)
            # if step != None and step[2]: 
            #     break
            print("hola")
            pygame.time.delay(120)

class IA():
    def __init__(self, juego):
        self.juego = juego
        self.path = None
        self.Q = {}

        ### Completar

    def set_path(self, path):
        self.path = path

    # Juega al juego hasta que este termine, cada vez que mueve (en cada step) decide cual es la mejor accion segun el diccionario Q.
    def jugar(self):
        while True:
            direcion_nueva = random.choice([0, 1, 2])
            step = self.juego.step(direcion_nueva)
            print(step)
            if step != None and step[2]: 
                break
            pygame.time.delay(300)

    # Juega el juego muchas veces y en cada vez completa la informacion de la tabla Q, en base al aprendizaje observado.
    def entrenar(self):
        partidas = 0
        max_partidas = 450000  # Cambiar este valor a un número mayor para entrenar más partidas
        for i in range(300000):
            jugando = True
            estado_anterior = self.juego.reset()

            if estado_anterior not in self.Q:
                self.Q[estado_anterior] = [0, 0, 0]

            while jugando:
                accion = self.get_max_action(self.Q[estado_anterior])
                estado, jugando, recompensa = self.juego.step(accion)

                if estado not in self.Q:
                    self.Q[estado] = [0, 0, 0]

                best_action = max(self.Q[estado])
                self.Q[estado_anterior][accion] += 0.05 * (recompensa - self.Q[estado_anterior][accion] + best_action)
                estado_anterior = estado

            i += 1
            print(partidas)
        print("Entrenamiento completado")
        self.save()

    def save(self):
        if self.path is not None:
            with open(self.path, 'wb') as f:
                pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        if self.path is not None:
            with open(self.path, 'rb') as f:
                self.Q = pickle.load(f)