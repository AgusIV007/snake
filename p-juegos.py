# En este archivo tenemos la clase que representa el juego a programar, es importante que siga la interfaz que tiene esta clase, o sea que tenga las funciones que hay en este archivo.

import pygame 

class Snake():
    def __init__(self, tamano):
        self.tamano = tamano

        ### Completar

        self.reset()

    # Reinicia el juego:
    #   - Pone la longitud de la serpiente en 1.
    #   - Coloca la serpiente en un lugar random.
    #   - Pone la fruta en una posicion random
    def reset(self):
        ### Completar
        pass

    # Mueve al jugador una vez, en fuincion a la accion realizada.
    # Devuelve 3 cosas:
    #   - El nuevo estado del juego
    #   - Si el juego termino o no (o sea si la serpiente murio o no)
    #   - La recompenza de la accion realizada (0 si no pasa nada, 1 si agarro una fruta, -1 si perdio)
    # Recordatorio: un estado es una lista de 11 numeros bienarios (1 o 0), cada uno de estos bits indican si se cumple una condicion o no (estas 11 condiciones estan detalladas en el informe).
    def step(self, accion):
        assert accion in {0,1,2}, "Accion invalida"     # Chequea que la accion sea valida (0 = sigue derecho, 1 = dobla a la izquierda, 2 = dobla a la derecha)

        estado_nuevo = None ### Completar
        recompenza = None   ### Completar
        termino = None      ### Completar
        ### Completar
        
        self.render()
        return estado_nuevo, recompenza, termino
    
    
    # Actualiza la informacion que se muestra en pantalla usando pygame.
    def render(self):
        ### Completar
        pass

