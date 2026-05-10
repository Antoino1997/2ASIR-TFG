# game/pieces.py

# random lo usamos para elegir una pieza aleatoria al crear una nueva
import random

# Diccionario con todas las piezas del Tetris y sus rotaciones
# cada pieza es una lista de matrices donde cada matriz es una rotación distinta
# 1 = hay bloque, 0 = celda vacía
PIECES = {
    # Pieza I — solo tiene 2 rotaciones: horizontal y vertical
    'I': [
        # Horizontal: una fila de 4 bloques
        [[1, 1, 1, 1]],
        # Vertical: una columna de 4 bloques
        [[1],
         [1],
         [1],
         [1]]
    ],
    # Pieza O — cuadrado 2x2, solo tiene 1 rotación porque es simétrica
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    # Pieza T — tiene 4 rotaciones (0°, 90°, 180°, 270°)
    'T': [
        # 0°
        [[0, 1, 0],
         [1, 1, 1]],
        # 90°
        [[1, 0],
         [1, 1],
         [1, 0]],
        # 180°
        [[1, 1, 1],
         [0, 1, 0]],
        # 270°
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    # Pieza S — tiene 2 rotaciones
    'S': [
        # Horizontal
        [[0, 1, 1],
         [1, 1, 0]],
        # Vertical
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    # Pieza Z — tiene 2 rotaciones, es el espejo de la S
    'Z': [
        # Horizontal
        [[1, 1, 0],
         [0, 1, 1]],
        # Vertical
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    # Pieza J — tiene 4 rotaciones
    'J': [
        # 0°
        [[1, 0, 0],
         [1, 1, 1]],
        # 90°
        [[1, 1],
         [1, 0],
         [1, 0]],
        # 180°
        [[1, 1, 1],
         [0, 0, 1]],
        # 270°
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    # Pieza L — tiene 4 rotaciones, es el espejo de la J
    'L': [
        # 0°
        [[0, 0, 1],
         [1, 1, 1]],
        # 90°
        [[1, 0],
         [1, 0],
         [1, 1]],
        # 180°
        [[1, 1, 1],
         [1, 0, 0]],
        # 270°
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

class Piece:
    def __init__(self, piece_type=None):
        if piece_type is None:
            # Si no se especifica tipo elegimos uno al azar de las 7 piezas disponibles
            self.type = random.choice(list(PIECES.keys()))
        else:
            # Si se especifica tipo lo usamos — útil para tests o para la pieza preview
            self.type = piece_type

        # Empezamos siempre en la primera rotación (índice 0)
        self.rotation = 0
        # Guardamos la matriz de la rotación actual para no tener que recalcularla cada vez
        self.shape = PIECES[self.type][self.rotation]
        # Posición inicial en el tablero — columna 3 para que aparezca aproximadamente centrada
        self.x = 3
        # Fila 0 = arriba del tablero, donde aparecen las piezas nuevas
        self.y = 0

    def rotate(self):
        """Rotar la pieza al siguiente estado"""
        rotations = PIECES[self.type]
        # Avanzamos al siguiente índice de rotación de forma circular
        # si estamos en la última rotación, volvemos a la primera
        self.rotation = (self.rotation + 1) % len(rotations)
        # Actualizamos la forma con la nueva rotación
        self.shape = rotations[self.rotation]

    def get_shape(self):
        """Obtener la forma actual de la pieza"""
        # Devuelve la matriz de la rotación actual
        return self.shape

    def get_positions(self):
        """Obtener las posiciones absolutas de los bloques de la pieza"""
        positions = []
        # Recorremos cada celda de la matriz de la pieza
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # si la celda es 1 (hay bloque)
                    # Sumamos la posición relativa de la matriz a la posición
                    # absoluta de la pieza en el tablero para obtener
                    # las coordenadas reales donde está cada bloque
                    positions.append((self.x + col_idx, self.y + row_idx))
        return positions