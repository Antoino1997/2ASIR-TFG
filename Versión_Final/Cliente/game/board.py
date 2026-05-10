# game/board.py

# Importamos solo las constantes que necesita este fichero — buena práctica
# en vez de importar todo con *
from config import BOARD_WIDTH, BOARD_HEIGHT

class Board:
    def __init__(self):
        # Guardamos las dimensiones del tablero como atributos del objeto
        self.width  = BOARD_WIDTH   # 10 columnas
        self.height = BOARD_HEIGHT  # 20 filas

        # Creamos la cuadrícula vacía como una lista de listas
        # grid[fila][columna] — None significa celda vacía
        # cuando hay un bloque guardamos el tipo de pieza ('I', 'O', 'T'...)
        # para saber de qué color pintarlo después
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def is_valid_position(self, piece):
        """Verificar si la pieza está en una posición válida"""
        # Obtenemos las coordenadas absolutas de cada bloque de la pieza
        positions = piece.get_positions()

        for x, y in positions:
            # Comprobamos que el bloque no se sale por los lados ni por abajo
            if x < 0 or x >= self.width or y >= self.height:
                return False

            # Comprobamos que la celda no está ya ocupada por otro bloque
            # y >= 0 porque cuando la pieza acaba de aparecer puede tener
            # bloques con y negativa (por encima del tablero visible)
            # e intentar acceder a grid[-1] daría la última fila, no un error
            if y >= 0 and self.grid[y][x] is not None:
                return False

        # Si ningún bloque ha fallado, la posición es válida
        return True

    def lock_piece(self, piece):
        """Fijar la pieza en el tablero"""
        positions = piece.get_positions()

        for x, y in positions:
            # Solo fijamos los bloques que están dentro del tablero visible
            # los que tienen y negativa están fuera y no se guardan
            if y >= 0:
                # Guardamos el tipo de pieza en la celda para saber su color al pintar
                self.grid[y][x] = piece.type

    def clear_lines(self):
        """Eliminar líneas completas y devolver cantidad eliminada"""
        lines_cleared = 0
        new_grid = []

        for row in self.grid:
            if None in row:
                # La fila tiene al menos un hueco — la conservamos
                new_grid.append(row)
            else:
                # La fila está completamente llena — la eliminamos y contamos
                lines_cleared += 1

        # Por cada línea eliminada añadimos una fila vacía arriba del todo
        # esto hace que el resto de bloques "bajen" visualmente
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(self.width)])

        # Reemplazamos el tablero con la versión sin las líneas completas
        self.grid = new_grid
        return lines_cleared

    def is_game_over(self):
        """Verificar si hay bloques en la primera fila"""
        # Si cualquier celda de la fila 0 (la de arriba) tiene un bloque
        # significa que las piezas han llegado al tope — game over
        return any(cell is not None for cell in self.grid[0])

    def reset(self):
        """Reiniciar el tablero"""
        # Recreamos la cuadrícula vacía — igual que en __init__
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]