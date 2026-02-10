"""
TETRIS STANDALONE
Juego completo de Tetris en un solo archivo
Sin conexión a servidor - Solo se puede jugar localmente
"""

import pygame
import random
import sys

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Dimensiones de la ventana
SCREEN_WIDTH = 800      # Ancho de la ventana en píxeles
SCREEN_HEIGHT = 700     # Alto de la ventana en píxeles

# Dimensiones del tablero de juego
BOARD_WIDTH = 10        # 10 columnas
BOARD_HEIGHT = 20       # 20 filas
BLOCK_SIZE = 30         # Cada bloque mide 30x30 píxeles

# Posición del tablero en la pantalla
BOARD_X = 50            # Margen izquierdo
BOARD_Y = 30            # Margen superior

# Colores (formato RGB: Red, Green, Blue)
BLACK = (0, 0, 0)           # Fondo
WHITE = (255, 255, 255)     # Texto y bordes
GRAY = (128, 128, 128)      # Grid del tablero
CYAN = (0, 255, 255)        # Pieza I
YELLOW = (255, 255, 0)      # Pieza O
MAGENTA = (255, 0, 255)     # Pieza T
GREEN = (0, 255, 0)         # Pieza S
RED = (255, 0, 0)           # Pieza Z
BLUE = (0, 0, 255)          # Pieza J
ORANGE = (255, 165, 0)      # Pieza L

# Colores asignados a cada tipo de pieza
PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': MAGENTA,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# Velocidad del juego
FPS = 60                    # Frames por segundo
FALL_SPEED = 500            # Milisegundos entre cada caída automática

# ============================================================================
# FORMAS DE LAS PIEZAS
# ============================================================================

# Cada pieza tiene una o más rotaciones
# 1 = bloque lleno, 0 = espacio vacío
PIECES = {
    'I': [
        # Horizontal
        [[1, 1, 1, 1]],
        # Vertical
        [[1],
         [1],
         [1],
         [1]]
    ],
    'O': [
        # Solo una rotación (cuadrado)
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        # 0 grados
        [[0, 1, 0],
         [1, 1, 1]],
        # 90 grados
        [[1, 0],
         [1, 1],
         [1, 0]],
        # 180 grados
        [[1, 1, 1],
         [0, 1, 0]],
        # 270 grados
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'S': [
        # Horizontal
        [[0, 1, 1],
         [1, 1, 0]],
        # Vertical
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        # Horizontal
        [[1, 1, 0],
         [0, 1, 1]],
        # Vertical
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        # 0 grados
        [[1, 0, 0],
         [1, 1, 1]],
        # 90 grados
        [[1, 1],
         [1, 0],
         [1, 0]],
        # 180 grados
        [[1, 1, 1],
         [0, 0, 1]],
        # 270 grados
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        # 0 grados
        [[0, 0, 1],
         [1, 1, 1]],
        # 90 grados
        [[1, 0],
         [1, 0],
         [1, 1]],
        # 180 grados
        [[1, 1, 1],
         [1, 0, 0]],
        # 270 grados
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

# ============================================================================
# CLASE PIECE (PIEZA)
# ============================================================================

class Piece:
    """Representa una pieza individual del Tetris"""

    def __init__(self, piece_type=None):
        """
        Inicializa una pieza
        piece_type: Tipo de pieza ('I', 'O', 'T', etc.) o None para aleatorio
        """
        # Si no se especifica tipo, elegir uno al azar
        if piece_type is None:
            self.type = random.choice(list(PIECES.keys()))
        else:
            self.type = piece_type

        self.rotation = 0                           # Índice de rotación actual (0, 1, 2, 3)
        self.rotations = PIECES[self.type]          # Lista de todas las rotaciones de esta pieza
        self.shape = self.rotations[self.rotation]  # Forma actual (matriz)
        self.x = 3                                  # Posición X inicial (columna 3)
        self.y = 0                                  # Posición Y inicial (fila 0 = arriba)

    def rotate(self):
        """Rota la pieza al siguiente estado de rotación"""
        # Avanzar al siguiente índice de rotación (circular)
        self.rotation = (self.rotation + 1) % len(self.rotations)
        # Actualizar la forma según la nueva rotación
        self.shape = self.rotations[self.rotation]

    def get_positions(self):
        """
        Devuelve las posiciones absolutas de todos los bloques de la pieza
        Returns: Lista de tuplas (x, y)
        """
        positions = []
        # Recorrer cada celda de la matriz de la pieza
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:  # Si hay un bloque (1)
                    # Calcular posición absoluta: posición de la pieza + offset en la matriz
                    positions.append((self.x + col_idx, self.y + row_idx))
        return positions

# ============================================================================
# CLASE BOARD (TABLERO)
# ============================================================================

class Board:
    """Representa el tablero de juego donde caen las piezas"""

    def __init__(self):
        """Inicializa un tablero vacío"""
        self.width = BOARD_WIDTH    # 10 columnas
        self.height = BOARD_HEIGHT  # 20 filas
        # Crear matriz vacía: None significa celda vacía
        # grid[fila][columna]
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def is_valid_position(self, piece):
        """
        Verifica si una pieza está en una posición válida
        Returns: True si es válida, False si hay colisión
        """
        positions = piece.get_positions()

        for x, y in positions:
            # Verificar límites horizontales (izquierda y derecha)
            if x < 0 or x >= self.width:
                return False

            # Verificar límite inferior
            if y >= self.height:
                return False

            # Verificar colisión con bloques existentes
            # (y >= 0 porque las piezas nuevas pueden estar parcialmente arriba)
            if y >= 0 and self.grid[y][x] is not None:
                return False

        return True

    def lock_piece(self, piece):
        """
        Fija una pieza en el tablero (la convierte en bloques estáticos)
        """
        positions = piece.get_positions()

        for x, y in positions:
            if y >= 0:  # Solo fijar bloques que estén dentro del tablero
                # Guardar el tipo de pieza para saber qué color usar
                self.grid[y][x] = piece.type

    def clear_lines(self):
        """
        Elimina las líneas completas y devuelve cuántas se eliminaron
        Returns: Número de líneas eliminadas
        """
        lines_cleared = 0
        new_grid = []

        # Recorrer todas las filas
        for row in self.grid:
            # Si la fila tiene algún None (espacio vacío), no está completa
            if None in row:
                new_grid.append(row)
            else:
                # Fila completa - no la agregamos (se elimina)
                lines_cleared += 1

        # Agregar filas vacías arriba por cada línea eliminada
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(self.width)])

        self.grid = new_grid
        return lines_cleared

    def is_game_over(self):
        """
        Verifica si hay bloques en la primera fila (game over)
        Returns: True si game over, False si puede continuar
        """
        # Si hay algún bloque en la fila superior (y=0), es game over
        return any(cell is not None for cell in self.grid[0])

    def reset(self):
        """Reinicia el tablero a vacío"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

# ============================================================================
# CLASE TETRIS (LÓGICA DEL JUEGO)
# ============================================================================

class Tetris:
    """Gestiona toda la lógica del juego"""

    def __init__(self):
        """Inicializa una nueva partida"""
        self.board = Board()                # Tablero de juego
        self.current_piece = Piece()        # Pieza que está cayendo
        self.next_piece = Piece()           # Siguiente pieza (preview)
        self.score = 0                      # Puntuación actual
        self.lines_cleared = 0              # Total de líneas eliminadas
        self.game_over = False              # Estado del juego

        self.last_fall_time = pygame.time.get_ticks()  # Timestamp de última caída
        self.fall_speed = FALL_SPEED                    # Velocidad de caída

    def move_left(self):
        """Intenta mover la pieza actual hacia la izquierda"""
        self.current_piece.x -= 1           # Mover una posición a la izquierda
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x += 1       # Revertir si hay colisión

    def move_right(self):
        """Intenta mover la pieza actual hacia la derecha"""
        self.current_piece.x += 1           # Mover una posición a la derecha
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x -= 1       # Revertir si hay colisión

    def move_down(self):
        """
        Intenta mover la pieza hacia abajo
        Returns: True si se movió, False si se fijó
        """
        self.current_piece.y += 1           # Bajar una posición
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.y -= 1       # Revertir
            self.lock_piece()               # Fijar la pieza
            return False
        return True

    def hard_drop(self):
        """Deja caer la pieza instantáneamente hasta el fondo"""
        # Seguir bajando hasta que no se pueda más
        while self.move_down():
            pass

    def rotate_piece(self):
        """Intenta rotar la pieza actual con sistema de wall kicks"""
        # Guardar estado actual por si hay que revertir
        old_rotation = self.current_piece.rotation
        old_shape = self.current_piece.shape
        old_x = self.current_piece.x
        old_y = self.current_piece.y

        # Intentar rotar
        self.current_piece.rotate()

        # Si la rotación es válida, listo
        if self.board.is_valid_position(self.current_piece):
            return

        # Si no es válida, intentar "wall kicks" (empujar la pieza)
        # Wall kicks = intentar mover la pieza a los lados antes de cancelar rotación

        # Para la pieza I necesitamos más desplazamientos
        if self.current_piece.type == 'I':
            kick_tests = [
                (1, 0), (-1, 0), (2, 0), (-2, 0), (3, 0), (-3, 0),
                (0, -1), (1, -1), (-1, -1),
            ]
        else:
            kick_tests = [
                (1, 0), (-1, 0), (2, 0), (-2, 0),
                (0, -1), (1, -1), (-1, -1),
            ]

        # Probar cada desplazamiento
        for dx, dy in kick_tests:
            self.current_piece.x = old_x + dx
            self.current_piece.y = old_y + dy

            if self.board.is_valid_position(self.current_piece):
                return  # ¡Funcionó con este desplazamiento!

        # Ningún kick funcionó - revertir rotación completamente
        self.current_piece.rotation = old_rotation
        self.current_piece.shape = old_shape
        self.current_piece.x = old_x
        self.current_piece.y = old_y

    def lock_piece(self):
        """Fija la pieza actual y genera una nueva"""
        # Fijar la pieza en el tablero
        self.board.lock_piece(self.current_piece)

        # Limpiar líneas completas y actualizar puntuación
        lines = self.board.clear_lines()
        if lines > 0:
            self.lines_cleared += lines
            # Sistema de puntuación: más líneas = más puntos
            # 1 línea = 100, 2 líneas = 400, 3 = 900, 4 = 1600
            self.score += lines * 100 * lines

        # Verificar game over
        if self.board.is_game_over():
            self.game_over = True
            return

        # Generar nueva pieza: la "siguiente" pasa a ser la actual
        self.current_piece = self.next_piece
        self.next_piece = Piece()

        # Si la nueva pieza no cabe, game over
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True

    def update(self):
        """Actualiza el estado del juego (caída automática)"""
        if self.game_over:
            return

        # Obtener tiempo actual
        current_time = pygame.time.get_ticks()

        # Si ha pasado suficiente tiempo, bajar la pieza automáticamente
        if current_time - self.last_fall_time > self.fall_speed:
            self.move_down()
            self.last_fall_time = current_time

    def reset(self):
        """Reinicia el juego a estado inicial"""
        self.board.reset()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.last_fall_time = pygame.time.get_ticks()

# ============================================================================
# FUNCIONES DE RENDERIZADO
# ============================================================================

def draw_board(screen, board):
    """Dibuja el tablero y los bloques fijos"""
    # Calcular dimensiones del tablero en píxeles
    board_width = BOARD_WIDTH * BLOCK_SIZE
    board_height = BOARD_HEIGHT * BLOCK_SIZE

    # Dibujar borde del tablero
    pygame.draw.rect(screen, GRAY,
                     (BOARD_X, BOARD_Y, board_width, board_height), 2)

    # Dibujar cada bloque fijo del tablero
    for row_idx, row in enumerate(board.grid):
        for col_idx, cell in enumerate(row):
            if cell is not None:  # Si hay un bloque
                draw_block(screen, col_idx, row_idx, PIECE_COLORS[cell])

def draw_piece(screen, piece):
    """Dibuja la pieza actual que está cayendo"""
    positions = piece.get_positions()
    color = PIECE_COLORS[piece.type]

    for x, y in positions:
        if y >= 0:  # Solo dibujar bloques visibles
            draw_block(screen, x, y, color)

def draw_block(screen, x, y, color):
    """Dibuja un bloque individual en una posición del tablero"""
    # Calcular posición en píxeles
    pixel_x = BOARD_X + x * BLOCK_SIZE
    pixel_y = BOARD_Y + y * BLOCK_SIZE

    # Dibujar bloque relleno
    pygame.draw.rect(screen, color,
                     (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))
    # Dibujar borde del bloque
    pygame.draw.rect(screen, WHITE,
                     (pixel_x, pixel_y, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_next_piece(screen, piece, font):
    """Dibuja la siguiente pieza (preview)"""
    next_x = BOARD_X + BOARD_WIDTH * BLOCK_SIZE + 50
    next_y = 100

    # Título
    text = font.render("Siguiente:", True, WHITE)
    screen.blit(text, (next_x, next_y - 30))

    # Dibujar la pieza
    color = PIECE_COLORS[piece.type]
    for row_idx, row in enumerate(piece.shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pixel_x = next_x + col_idx * BLOCK_SIZE
                pixel_y = next_y + row_idx * BLOCK_SIZE
                pygame.draw.rect(screen, color,
                                 (pixel_x, pixel_y, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

def draw_info(screen, tetris, font, small_font):
    """Dibuja información del juego (puntuación, líneas, controles)"""
    info_x = BOARD_X + BOARD_WIDTH * BLOCK_SIZE + 50
    info_y = 250

    # Puntuación
    score_text = font.render(f"Puntos: {tetris.score}", True, WHITE)
    screen.blit(score_text, (info_x, info_y))

    # Líneas eliminadas
    lines_text = small_font.render(f"Líneas: {tetris.lines_cleared}", True, WHITE)
    screen.blit(lines_text, (info_x, info_y + 40))

    # Controles
    controls_y = info_y + 100
    controls = [
        "Controles:",
        "IZQUIERDA/DERECHA: Mover",
        "ABAJO: Bajar rapido",
        "ARRIBA: Rotar",
        "ESPACIO: Caida instantanea",
        "R: Reiniciar",
        "ESC: Menu"
    ]

    for i, control in enumerate(controls):
        text = small_font.render(control, True, GRAY)
        screen.blit(text, (info_x, controls_y + i * 25))

def draw_game_over(screen, score, font):
    """Dibuja la pantalla de Game Over"""
    # Overlay semi-transparente
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Textos
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Puntuacion final: {score}", True, WHITE)
    restart_text = font.render("Presiona R para reiniciar", True, WHITE)
    menu_text = font.render("o ESC para volver al menu", True, WHITE)

    # Centrar textos
    text_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2

    screen.blit(game_over_text, (text_x, SCREEN_HEIGHT // 2 - 80))
    screen.blit(score_text, (text_x, SCREEN_HEIGHT // 2 - 20))
    screen.blit(restart_text, (text_x, SCREEN_HEIGHT // 2 + 40))
    screen.blit(menu_text, (text_x, SCREEN_HEIGHT // 2 + 80))

# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

def draw_menu(screen, font, small_font):
    """Dibuja el menú principal"""
    screen.fill(BLACK)

    # Título
    title = font.render("T E T R I S", True, CYAN)
    title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
    screen.blit(title, (title_x, 150))

    # Opciones del menú
    play_text = font.render("1. JUGAR", True, WHITE)
    controls_text = font.render("2. CONTROLES", True, WHITE)
    exit_text = font.render("3. SALIR", True, WHITE)

    menu_x = SCREEN_WIDTH // 2 - play_text.get_width() // 2

    screen.blit(play_text, (menu_x, 300))
    screen.blit(controls_text, (menu_x, 370))
    screen.blit(exit_text, (menu_x, 440))

    # Instrucción
    instruction = small_font.render("Presiona 1, 2 o 3", True, GRAY)
    instr_x = SCREEN_WIDTH // 2 - instruction.get_width() // 2
    screen.blit(instruction, (instr_x, 550))

def draw_controls_screen(screen, font, small_font):
    """Dibuja la pantalla de controles"""
    screen.fill(BLACK)

    # Título
    title = font.render("CONTROLES", True, CYAN)
    title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
    screen.blit(title, (title_x, 75))

    # Lista de controles
    controls = [
        "",
        "IZQUIERDA/DERECHA - Mover pieza",
        "ABAJO - Bajar mas rapido",
        "ARRIBA - Rotar pieza",
        "ESPACIO - Caida instantanea",
        "R - Reiniciar partida",
        "ESC - Volver al menu",
        "",
        "PUNTUACION:",
        "1 linea = 100 puntos",
        "2 lineas = 400 puntos",
        "3 lineas = 900 puntos",
        "4 lineas = 1600 puntos (TETRIS!)",
    ]

    y = 100
    for control in controls:
        text = small_font.render(control, True, WHITE if control else GRAY)
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        screen.blit(text, (text_x, y))
        y += 35

    # Volver
    back_text = small_font.render("Presiona ESC para volver", True, GRAY)
    back_x = SCREEN_WIDTH // 2 - back_text.get_width() // 2
    screen.blit(back_text, (back_x, 600))

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del juego"""
    # Inicializar Pygame
    pygame.init()

    # Crear ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Reloj para controlar FPS
    clock = pygame.time.Clock()

    # Fuentes
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Estados del juego
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_CONTROLS = "controls"

    # Estado inicial
    state = STATE_MENU
    tetris = None

    # Bucle principal del juego
    running = True
    while running:
        clock.tick(FPS)  # Limitar a 60 FPS

        # Procesar eventos
        for event in pygame.event.get():
            # Evento: cerrar ventana
            if event.type == pygame.QUIT:
                running = False

            # Evento: tecla presionada
            if event.type == pygame.KEYDOWN:
                # --- MENÚ PRINCIPAL ---
                if state == STATE_MENU:
                    if event.key == pygame.K_1:  # Jugar
                        state = STATE_PLAYING
                        tetris = Tetris()  # Crear nuevo juego
                    elif event.key == pygame.K_2:  # Controles
                        state = STATE_CONTROLS
                    elif event.key == pygame.K_3:  # Salir
                        running = False

                # --- PANTALLA DE CONTROLES ---
                elif state == STATE_CONTROLS:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                # --- JUGANDO ---
                elif state == STATE_PLAYING:
                    if not tetris.game_over:
                        # Controles del juego
                        if event.key == pygame.K_LEFT:
                            tetris.move_left()
                        elif event.key == pygame.K_RIGHT:
                            tetris.move_right()
                        elif event.key == pygame.K_DOWN:
                            tetris.move_down()
                        elif event.key == pygame.K_UP:
                            tetris.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            tetris.hard_drop()
                        elif event.key == pygame.K_ESCAPE:
                            state = STATE_MENU
                    else:
                        # Game Over - opciones
                        if event.key == pygame.K_r:
                            tetris.reset()
                        elif event.key == pygame.K_ESCAPE:
                            state = STATE_MENU

        # Actualizar lógica del juego
        if state == STATE_PLAYING and tetris:
            tetris.update()

        # Dibujar según el estado
        screen.fill(BLACK)

        if state == STATE_MENU:
            draw_menu(screen, font, small_font)

        elif state == STATE_CONTROLS:
            draw_controls_screen(screen, font, small_font)

        elif state == STATE_PLAYING:
            draw_board(screen, tetris.board)
            draw_piece(screen, tetris.current_piece)
            draw_next_piece(screen, tetris.next_piece, small_font)
            draw_info(screen, tetris, font, small_font)

            if tetris.game_over:
                draw_game_over(screen, tetris.score, font)

        # Actualizar pantalla
        pygame.display.flip()

    # Salir
    pygame.quit()
    sys.exit()

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()