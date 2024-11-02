# En este archivo tenemos las clases que representan jugadores
import pickle

class Random():
    def __init__(self, juego):
        self.juego = None
        ### Completar si hace falta

    # Juega al juego(de manera aleatoria) hasta que este termine
    def jugar(self):
        ### Completar
        pass

    def entrenar(self):
        raise NotImplementedError


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
        ### Completar
        pass

    # Juega el juego muchas veces y en cada vez completa la informacion de la tabla Q, en base al aprendizaje observado.
    def entrenar(self):
        ### Completar
        pass

    def save(self):
        if self.path is not None:
            with open(self.path, 'wb') as f:
                pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        if self.path is not None:
            with open(self.path, 'rb') as f:
                self.Q = pickle.load(f)