# game/renderer.py

import pygame
# Importamos todas las constantes de config: colores, tamaños, dimensiones
from config import *

class Renderer:
    def __init__(self, screen):
        # Guardamos la referencia a la pantalla donde vamos a dibujar todo
        self.screen = screen
        # Fuente normal para textos importantes como la puntuación
        self.font = pygame.font.Font(None, 36)
        # Fuente más pequeña para textos secundarios como controles y líneas
        self.small_font = pygame.font.Font(None, 24)

        # Posición en píxeles donde empieza el tablero dentro de la ventana
        # esto deja un margen de 50px a la izquierda y arriba
        self.board_x = 50
        self.board_y = 50

    def draw_board(self, board):
        """Dibujar el tablero y los bloques fijos"""
        # Calculamos el tamaño total del tablero en píxeles
        board_width  = board.width  * BLOCK_SIZE
        board_height = board.height * BLOCK_SIZE

        # Dibujamos el borde del tablero en gris con grosor 2
        # el último parámetro es el grosor — si fuera 0 lo rellenaría entero
        pygame.draw.rect(self.screen, GRAY,
                         (self.board_x, self.board_y, board_width, board_height), 2)

        # Recorremos todas las celdas de la cuadrícula
        for row_idx, row in enumerate(board.grid):
            for col_idx, cell in enumerate(row):
                if cell is not None:
                    # Si la celda tiene un valor es que hay un bloque fijo
                    # el valor es el tipo de pieza ('I', 'T', etc.) para saber el color
                    self.draw_block(col_idx, row_idx, PIECE_COLORS[cell])

    def draw_piece(self, piece):
        """Dibujar la pieza actual que está cayendo"""
        positions = piece.get_positions()
        # Cogemos el color según el tipo de pieza
        color = PIECE_COLORS[piece.type]

        for x, y in positions:
            # Solo dibujamos los bloques que están dentro del tablero visible
            # los que tienen y negativa están por encima del tablero y no se pintan
            if y >= 0:
                self.draw_block(x, y, color)

    def draw_block(self, x, y, color):
        """Dibujar un bloque individual en una posición del tablero"""
        # Convertimos las coordenadas del tablero a píxeles de pantalla
        pixel_x = self.board_x + x * BLOCK_SIZE
        pixel_y = self.board_y + y * BLOCK_SIZE

        # Dibujamos el relleno del bloque con 1px de margen por cada lado
        # para que se vea la separación entre bloques adyacentes
        pygame.draw.rect(self.screen, color,
                         (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        # Dibujamos el borde blanco del bloque con grosor 1
        pygame.draw.rect(self.screen, WHITE,
                         (pixel_x, pixel_y, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next_piece(self, piece):
        """Dibujar la vista previa de la siguiente pieza"""
        # Posicionamos la preview a la derecha del tablero
        next_x = self.board_x + BOARD_WIDTH * BLOCK_SIZE + 50
        next_y = 100

        # Etiqueta "Siguiente:" encima de la pieza
        text = self.small_font.render("Siguiente:", True, WHITE)
        self.screen.blit(text, (next_x, next_y - 30))

        color = PIECE_COLORS[piece.type]
        # Recorremos la matriz de la pieza para dibujar cada bloque
        for row_idx, row in enumerate(piece.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    # Las posiciones son relativas al área de preview, no al tablero
                    pixel_x = next_x + col_idx * BLOCK_SIZE
                    pixel_y = next_y + row_idx * BLOCK_SIZE
                    pygame.draw.rect(self.screen, color,
                                     (pixel_x, pixel_y, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_info(self, tetris, username):
        """Dibujar el panel de información a la derecha del tablero"""
        # Posicionamos el panel justo a la derecha del tablero
        info_x = self.board_x + BOARD_WIDTH * BLOCK_SIZE + 50
        info_y = 250

        # Nombre del usuario que está jugando
        user_text = self.small_font.render(f"Usuario: {username}", True, WHITE)
        self.screen.blit(user_text, (info_x, info_y))

        # Puntuación actual en fuente grande para que sea fácil de leer
        score_text = self.font.render(f"Puntos: {tetris.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, info_y + 40))

        # Total de líneas eliminadas en esta partida
        lines_text = self.small_font.render(f"Líneas: {tetris.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (info_x, info_y + 80))

        # Lista de controles — cada línea se dibuja 25px más abajo que la anterior
        controls_y = info_y + 150
        controls = [
            "Controles:",
            "IZQUIERDA/DERECHA : Mover",
            "ABAJO : Bajar",
            "ARRIBA : Rotar",
            "ESPACIO : Caída rápida",
            "ESC : Salir"
        ]

        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, GRAY)
            self.screen.blit(text, (info_x, controls_y + i * 25))

    def draw_game_over(self, score):
        """Dibujar la pantalla de game over encima del juego"""
        # Creamos una superficie del tamaño de toda la ventana
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # set_alpha(200) la hace semi-transparente — 0 es invisible, 255 es opaco
        # así se ve el tablero oscurecido por debajo
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text     = self.font.render(f"Puntuación final: {score}", True, WHITE)
        restart_text   = self.small_font.render("Presiona R para reiniciar o ESC para salir", True, WHITE)

        # Centramos el texto "GAME OVER" horizontalmente
        # get_width() nos da el ancho del texto renderizado en píxeles
        text_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2

        self.screen.blit(game_over_text, (text_x, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(score_text,     (text_x, SCREEN_HEIGHT // 2))
        # El texto de reiniciar puede tener ancho distinto, lo centramos por separado
        self.screen.blit(restart_text,   (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 + 60))