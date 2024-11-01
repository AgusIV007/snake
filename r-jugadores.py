# En este archivo tenemos las clases que representan jugadores
import os
import pickle
import random

class Random():
    def __init__(self, juego):
        self.juego = juego

    def jugar(self):
        while True:  
            estado = self.juego.reset()
            jugando = True
            while jugando:
                accion = random.randint(0, 2)
                estado, jugando, recompensa = self.juego.step(accion)
                print(f"Estado: {estado}, Recompensa: {recompensa}")


    def entrenar(self):
        raise NotImplementedError


class IA():
    def __init__(self, juego):
        self.juego = juego
        self.path = os.path.join(os.path.dirname(__file__), 'train.pkl')  # Ruta predeterminada
        self.Q = {}
        self.load()

    def jugar(self):
        estado = self.juego.reset()
        jugando = True
        while jugando:
            if estado not in self.Q:
                self.Q[estado] = [0, 0, 0]

            accion = self.get_max_action(self.Q[estado])
            estado, jugando, recompensa = self.juego.step(accion)

    def entrenar(self):
        partidas = 0
        max_partidas = 450000  # Cambiar este valor a un número mayor para entrenar más partidas

        while partidas < max_partidas:
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

            partidas += 1
            print(partidas)
        print("Entrenamiento completado")
        self.save()  # Guardar el estado después del entrenamiento

    def get_max_action(self, state):
        max_value = max(state)
        if state[0] == state[1] == state[2]:
            return random.randint(0, 2)
        elif state[0] == state[1] == max_value:
            return random.choice([0, 1])
        elif state[0] == state[2] == max_value:
            return random.choice([0, 2])
        elif state[1] == state[2] == max_value:
            return random.choice([1, 2])

        return state.index(max_value)

    def set_path(self, path):
        self.path = path

    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                self.Q = pickle.load(f)
        else:
            print(f"No se encontró el archivo en {self.path}, iniciando con un Q vacío.")
