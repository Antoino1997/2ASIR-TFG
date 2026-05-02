# game/tetris.py
import pygame
from game.board import Board
from game.pieces import Piece, PIECES

class Tetris:
    def __init__(self, api_client):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.api_client = api_client

        self.last_fall_time = pygame.time.get_ticks()
        self.fall_speed = 500  # milisegundos

    def move_left(self):
        """Mover pieza a la izquierda"""
        self.current_piece.x -= 1
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x += 1

    def move_right(self):
        """Mover pieza a la derecha"""
        self.current_piece.x += 1
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= 1

    def move_down(self):
        """Mover pieza hacia abajo"""
        self.current_piece.y += 1
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.y -= 1
            self.lock_piece()
            return False
        return True

    def hard_drop(self):
        """Caída rápida hasta el fondo"""
        while self.move_down():
            pass

    def rotate_piece(self):
        """Rotar la pieza actual con wall kicks mejorados"""
        old_rotation = self.current_piece.rotation
        old_shape = self.current_piece.shape
        old_x = self.current_piece.x
        old_y = self.current_piece.y

        self.current_piece.rotate()

        if self.board.is_valid_position(self.current_piece):
            return

        if self.current_piece.type == 'I':
            kick_tests = [
                (1, 0),
                (-1, 0),
                (2, 0),
                (-2, 0),
                (3, 0),
                (-3, 0),
                (0, -1),
                (1, -1),
                (-1, -1),
            ]
        else:
            kick_tests = [
                (1, 0),
                (-1, 0),
                (2, 0),
                (-2, 0),
                (0, -1),
                (1, -1),
                (-1, -1),
            ]

        for dx, dy in kick_tests:
            self.current_piece.x = old_x + dx
            self.current_piece.y = old_y + dy

            if self.board.is_valid_position(self.current_piece):
                return

        self.current_piece.rotation = old_rotation
        self.current_piece.shape = old_shape
        self.current_piece.x = old_x
        self.current_piece.y = old_y

    def lock_piece(self):
        """Fijar la pieza actual y generar una nueva"""
        self.board.lock_piece(self.current_piece)

        lines = self.board.clear_lines()
        if lines > 0:
            self.lines_cleared += lines
            self.score += lines * 100 * lines

        if self.board.is_game_over():
            self.game_over = True
            self.save_score()
            return

        self.current_piece = self.next_piece
        self.next_piece = Piece()

        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
            self.save_score()

    def update(self):
        """Actualizar el juego (caída automática)"""
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time > self.fall_speed:
            self.move_down()
            self.last_fall_time = current_time

    def save_score(self):
        """Guardar puntuación en el servidor"""
        success, message = self.api_client.save_score(self.score)
        print(f"Guardando puntuación: {message}")

    def reset(self):
        """Reiniciar el juego"""
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.last_fall_time = pygame.time.get_ticks()