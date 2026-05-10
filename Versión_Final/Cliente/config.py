# config.py

# URL del servidor al que se conecta el cliente para login, guardar puntuaciones y ranking
SERVER_URL = "http://127.0.0.1:5000"

# Número de columnas del tablero de juego
BOARD_WIDTH = 10
# Número de filas del tablero de juego
BOARD_HEIGHT = 20
# Tamaño en píxeles de cada bloque individual
BLOCK_SIZE = 30

# Ancho total del tablero en píxeles (10 columnas × 30px = 300px)
BOARD_PIXEL_WIDTH = BOARD_WIDTH * BLOCK_SIZE
# Alto total del tablero en píxeles (20 filas × 30px = 600px)
BOARD_PIXEL_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE

# Espacio en píxeles alrededor del tablero
MARGIN = 50
# Ancho del panel derecho donde se muestra la puntuación, siguiente pieza y controles
INFO_PANEL_WIDTH = 250

# Ancho total de la ventana:
# margen izquierdo + tablero + margen central + panel info + margen derecho = 750px
SCREEN_WIDTH = MARGIN + BOARD_PIXEL_WIDTH + MARGIN + INFO_PANEL_WIDTH + MARGIN
# Alto total de la ventana:
# margen superior + tablero + margen inferior = 700px
SCREEN_HEIGHT = MARGIN + BOARD_PIXEL_HEIGHT + MARGIN

# Colores en formato RGB (Red, Green, Blue) con valores entre 0 y 255
BLACK   = (0, 0, 0)        # fondo de la pantalla
WHITE   = (255, 255, 255)  # bordes de los bloques y texto
GRAY    = (128, 128, 128)  # texto secundario y borde del tablero
RED     = (255, 0, 0)      # pieza Z
GREEN   = (0, 255, 0)      # pieza S
BLUE    = (0, 0, 255)      # pieza J
CYAN    = (0, 255, 255)    # pieza I
YELLOW  = (255, 255, 0)    # pieza O
MAGENTA = (255, 0, 255)    # pieza T
ORANGE  = (255, 165, 0)    # pieza L

# Diccionario que relaciona cada tipo de pieza con su color
# se usa en el renderer para saber de qué color pintar cada bloque
PIECE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': MAGENTA,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# Frames por segundo — controla la fluidez de la animación
FPS = 60
# Milisegundos entre cada caída automática de la pieza
# 500ms = la pieza baja una fila cada medio segundo
FALL_SPEED = 500