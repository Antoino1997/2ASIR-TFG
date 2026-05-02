# game/__init__.py
"""
Módulo del juego Tetris
Contiene la lógica principal, piezas, tablero y renderizado
"""

from .tetris import Tetris
from .pieces import Piece, PIECES
from .board import Board
from .renderer import Renderer

__all__ = ['Tetris', 'Piece', 'PIECES', 'Board', 'Renderer']