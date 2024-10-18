import sys
import pygame
from juegos import Snake
from juegos import Ventana
from jugadores import Random, IA
import threading

JUGADORES_PERMITIDOS = {"ia": IA, "random": Random}

def print_help():
    print("Como correr el script: \n")
    print("\t python main.py random si ./train.json")

if __name__ == "__main__":
    try:
        tipo_jugador = sys.argv[1].lower()
        entrenar = sys.argv[2].lower()
        file_path = sys.argv[3]
        
        # Crear el objeto juego antes de la ventana
        juego = Snake(16)  
        
        # Inicializar el jugador
        if tipo_jugador in JUGADORES_PERMITIDOS:
            jugador = JUGADORES_PERMITIDOS[tipo_jugador](juego)
        else:
            raise Exception("Nombre de jugador no conocido")
        ventana = Ventana()

        # Inicializar la ventana
        jugador_thread = threading.Thread(target=jugador.jugar)
        jugador_thread.start()

        # Ejecutar la ventana
        ventana.ejecutar(juego)
        
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos.")
        print_help()
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        print_help()
        sys.exit(1)
    if tipo_jugador in JUGADORES_PERMITIDOS:
        jugador = JUGADORES_PERMITIDOS[tipo_jugador](juego)
    else:
        raise Exception("Nombre de jugador no conocido")

    # Entrenar puede ser 'si' o 'no'
    if tipo_jugador == "ia":
        jugador.set_path(file_path)
        if entrenar in {"si", "true"}:
            jugador.entrenar()
            jugador.save()
        else:
            jugador.load()
    
    jugador.jugar()