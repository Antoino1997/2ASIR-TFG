# game/tetris.py

# pygame lo usamos solo para get_ticks() — nos da el tiempo en milisegundos
# desde que arrancó el programa, para controlar la caída automática
import pygame
# Importamos el tablero y las piezas que ya hemos comentado
from game.board import Board
from game.pieces import Piece, PIECES

class Tetris:
    def __init__(self, api_client):
        # El tablero donde caen y se fijan las piezas
        self.board = Board()
        # La pieza que está cayendo en este momento
        self.current_piece = Piece()
        # La siguiente pieza — se muestra en la preview del panel derecho
        self.next_piece = Piece()
        # Puntuación acumulada en esta partida
        self.score = 0
        # Total de líneas eliminadas en esta partida
        self.lines_cleared = 0
        # Flag que indica si la partida ha terminado
        self.game_over = False
        # Guardamos el api_client para poder enviar la puntuación al servidor al terminar
        self.api_client = api_client

        # Guardamos el momento actual en milisegundos como referencia para la caída automática
        self.last_fall_time = pygame.time.get_ticks()
        # Cada cuántos milisegundos baja la pieza una fila sola (500ms = 0.5 segundos)
        self.fall_speed = 500

    def move_left(self):
        """Mover pieza a la izquierda"""
        # Intentamos mover la pieza una columna a la izquierda
        self.current_piece.x -= 1
        # Si la nueva posición no es válida (choca con pared o bloque) revertimos
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x += 1

    def move_right(self):
        """Mover pieza a la derecha"""
        # Igual que move_left pero en dirección contraria
        self.current_piece.x += 1
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= 1

    def move_down(self):
        """Mover pieza hacia abajo"""
        # Intentamos bajar la pieza una fila
        self.current_piece.y += 1
        if not self.board.is_valid_position(self.current_piece):
            # Si no puede bajar más, revertimos y fijamos la pieza en el tablero
            self.current_piece.y -= 1
            self.lock_piece()
            return False  # devolvemos False para indicar que la pieza se ha fijado
        return True  # devolvemos True para indicar que la pieza se ha movido

    def hard_drop(self):
        """Caída rápida hasta el fondo"""
        # Seguimos bajando la pieza hasta que move_down devuelva False
        # es decir, hasta que toque fondo o un bloque
        while self.move_down():
            pass

    def rotate_piece(self):
        """Rotar la pieza actual con wall kicks"""
        # Guardamos el estado actual por si hay que revertir la rotación
        old_rotation = self.current_piece.rotation
        old_shape    = self.current_piece.shape
        old_x        = self.current_piece.x
        old_y        = self.current_piece.y

        # Intentamos rotar la pieza
        self.current_piece.rotate()

        # Si la rotación es válida tal cual, no hacemos nada más
        if self.board.is_valid_position(self.current_piece):
            return

        # Si la rotación choca, intentamos "wall kicks":
        # desplazamos la pieza ligeramente en distintas direcciones
        # para ver si cabe en alguna posición cercana

        # La pieza I es más larga y necesita probar más desplazamientos
        if self.current_piece.type == 'I':
            kick_tests = [
                (1, 0),   # 1 columna a la derecha
                (-1, 0),  # 1 columna a la izquierda
                (2, 0),   # 2 columnas a la derecha
                (-2, 0),  # 2 columnas a la izquierda
                (3, 0),   # 3 columnas a la derecha
                (-3, 0),  # 3 columnas a la izquierda
                (0, -1),  # 1 fila hacia arriba
                (1, -1),  # diagonal derecha-arriba
                (-1, -1), # diagonal izquierda-arriba
            ]
        else:
            # Para el resto de piezas con menos desplazamientos es suficiente
            kick_tests = [
                (1, 0),
                (-1, 0),
                (2, 0),
                (-2, 0),
                (0, -1),
                (1, -1),
                (-1, -1),
            ]

        # Probamos cada desplazamiento hasta encontrar uno que funcione
        for dx, dy in kick_tests:
            self.current_piece.x = old_x + dx
            self.current_piece.y = old_y + dy

            if self.board.is_valid_position(self.current_piece):
                # Encontramos una posición válida con este desplazamiento
                return

        # Si ningún wall kick funcionó, revertimos la rotación completamente
        self.current_piece.rotation = old_rotation
        self.current_piece.shape    = old_shape
        self.current_piece.x        = old_x
        self.current_piece.y        = old_y

    def lock_piece(self):
        """Fijar la pieza actual y generar una nueva"""
        # Fijamos la pieza en el tablero — sus bloques pasan a ser parte de la cuadrícula
        self.board.lock_piece(self.current_piece)

        # Comprobamos si se han completado líneas y actualizamos la puntuación
        lines = self.board.clear_lines()
        if lines > 0:
            self.lines_cleared += lines
            # Sistema de puntuación con bonus por líneas múltiples:
            # 1 línea = 100, 2 líneas = 400, 3 líneas = 900, 4 líneas = 1600
            self.score += lines * 100 * lines

        # Comprobamos si los bloques han llegado a la fila de arriba
        if self.board.is_game_over():
            self.game_over = True
            # Guardamos la puntuación en el servidor antes de terminar
            self.save_score()
            return

        # La pieza siguiente pasa a ser la actual
        self.current_piece = self.next_piece
        # Generamos una nueva pieza siguiente aleatoria
        self.next_piece = Piece()

        # Si la nueva pieza no cabe nada más aparecer, también es game over
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
            self.save_score()

    def update(self):
        """Actualizar el juego — gestiona la caída automática"""
        # Si la partida ha terminado no hacemos nada
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()
        # Comprobamos si ha pasado suficiente tiempo desde la última caída
        if current_time - self.last_fall_time > self.fall_speed:
            self.move_down()
            # Actualizamos el tiempo de referencia para la siguiente caída
            self.last_fall_time = current_time

    def save_score(self):
        """Guardar puntuación en el servidor al terminar la partida"""
        # Llamamos al api_client que se encarga de hacer la petición HTTP
        success, message = self.api_client.save_score(self.score)
        # Mostramos el resultado en la consola para depuración
        print(f"Guardando puntuación: {message}")

    def reset(self):
        """Reiniciar el juego a su estado inicial"""
        # Vaciamos el tablero
        self.board.reset()
        # Generamos piezas nuevas
        self.current_piece = Piece()
        self.next_piece    = Piece()
        # Reiniciamos contadores
        self.score         = 0
        self.lines_cleared = 0
        self.game_over     = False
        # Reiniciamos el temporizador de caída para que no caiga inmediatamente
        self.last_fall_time = pygame.time.get_ticks()