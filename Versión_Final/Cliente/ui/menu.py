# ui/menu.py

import pygame
import pygame_gui
from config import *

class Menu:
    def __init__(self, screen, api_client, username):
        # Guardamos la pantalla, el cliente API y el nombre del usuario logueado
        self.screen = screen
        self.api_client = api_client
        self.username = username

        # Obtenemos el tamaño real de la ventana para calcular posiciones
        screen_width, screen_height = screen.get_size()
        # El manager gestiona todos los elementos de la interfaz de pygame_gui
        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        # Precargamos la fuente monospace para evitar warnings al abrir instrucciones
        self.manager.preload_fonts([
            {'name': 'fira_code', 'point_size': 12, 'style': 'regular'},
            {'name': 'fira_code', 'point_size': 12, 'style': 'bold'}
        ])

        # Dimensiones del panel central con los botones
        panel_width = 400
        panel_height = 450
        # Calculamos la posición para que el panel quede centrado en la ventana
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        # Título del juego — lo ponemos 80px por encima del panel
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(panel_x, panel_y - 80, panel_width, 60),
            text='TETRIS',
            manager=self.manager
        )

        # Saludo personalizado con el nombre del usuario que ha iniciado sesión
        self.welcome_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(panel_x, panel_y - 20, panel_width, 40),
            text=f'Bienvenido, {username}',
            manager=self.manager
        )

        # Botón para iniciar una partida
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 40, panel_width - 100, 50),
            text='JUGAR',
            manager=self.manager
        )

        # Botón para ver el ranking global descargado del servidor
        self.ranking_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 110, panel_width - 100, 50),
            text='VER RANKING',
            manager=self.manager
        )

        # Botón para ver los controles y sistema de puntuación
        self.instructions_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 180, panel_width - 100, 50),
            text='INSTRUCCIONES',
            manager=self.manager
        )

        # Botón para cerrar el programa
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 250, panel_width - 100, 50),
            text='SALIR',
            manager=self.manager
        )

        # Panel emergente del ranking — empieza a None porque aún no se ha abierto
        self.ranking_panel = None
        self.showing_ranking = False  # flag para evitar abrir dos ventanas a la vez

        # Panel emergente de instrucciones — igual que el de ranking
        self.instructions_panel = None
        self.showing_instructions = False

    def run(self):
        """Ejecutar el menú principal"""
        clock = pygame.time.Clock()
        running = True
        action = None  # la acción que devolveremos a main.py al salir del bucle

        while running:
            # tiempo en segundos desde el último frame, necesario para pygame_gui
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        # Le decimos a main.py que el usuario quiere jugar
                        return 'play'

                    elif event.ui_element == self.ranking_button:
                        # Abrimos la ventana emergente con el ranking
                        self.show_ranking()

                    elif event.ui_element == self.instructions_button:
                        # Abrimos la ventana emergente con las instrucciones
                        self.show_instructions()

                    elif event.ui_element == self.exit_button:
                        return 'exit'

                    elif hasattr(event.ui_element, 'most_specific_combined_id'):
                        # Detectamos si se pulsó el botón cerrar de alguna ventana emergente
                        # most_specific_combined_id contiene el object_id que le dimos al botón
                        if 'close_ranking' in event.ui_element.most_specific_combined_id:
                            self.close_ranking()
                        elif 'close_instructions' in event.ui_element.most_specific_combined_id:
                            self.close_instructions()

                # Pasamos el evento a pygame_gui para que procese clicks, teclado, etc.
                self.manager.process_events(event)

            # Actualizamos el estado interno de pygame_gui
            self.manager.update(time_delta)

            # Dibujamos el fondo antes que la interfaz para que quede por debajo
            self.draw_background()
            # Dibujamos todos los elementos de la interfaz encima del fondo
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        return action

    def draw_background(self):
        """Dibujar fondo del menú con bloques decorativos arriba y abajo"""
        self.screen.fill(BLACK)

        screen_width, screen_height = self.screen.get_size()
        block_colors = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]
        block_size = 30
        gap = 30  # espacio entre bloques

        # Calculamos cuántos bloques caben en el ancho de la ventana
        num_blocks = screen_width // (block_size + gap)
        # Ancho total que ocupan todos los bloques con sus espacios
        total_width = num_blocks * (block_size + gap) - gap
        # Margen para centrar el conjunto de bloques horizontalmente
        margin = (screen_width - total_width) // 2

        for i in range(num_blocks):
            x = margin + i * (block_size + gap)
            # Rotamos los colores cíclicamente con el operador módulo
            color = block_colors[i % len(block_colors)]

            # Fila superior de bloques decorativos
            pygame.draw.rect(self.screen, color, (x, 20, block_size, block_size))
            pygame.draw.rect(self.screen, WHITE, (x, 20, block_size, block_size), 1)

            # Fila inferior — empezamos el color desplazado 3 posiciones para variar
            color2 = block_colors[(i + 3) % len(block_colors)]
            pygame.draw.rect(self.screen, color2, (x, screen_height - 50, block_size, block_size))
            pygame.draw.rect(self.screen, WHITE, (x, screen_height - 50, block_size, block_size), 1)

    def show_ranking(self):
        """Mostrar el ranking en una ventana emergente"""
        # Si ya está abierto no hacemos nada — evitamos abrir dos ventanas a la vez
        if self.showing_ranking:
            return

        self.showing_ranking = True

        # Pedimos el top 10 al servidor a través del api_client
        success, ranking = self.api_client.get_ranking(10)

        panel_width = 500
        panel_height = 500
        # Centramos la ventana emergente en la pantalla
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        # Creamos el panel contenedor de la ventana emergente
        self.ranking_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.manager
        )

        # Título de la ventana — las posiciones son relativas al panel, no a la pantalla
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 20, panel_width - 100, 40),
            text='TOP 10 RANKING GLOBAL',
            manager=self.manager,
            container=self.ranking_panel
        )

        # Si el servidor respondió bien mostramos el ranking, si no un mensaje de error
        if success and ranking:
            ranking_text = self.format_ranking(ranking)
        else:
            ranking_text = "No se pudo cargar el ranking\nVerifica tu conexión al servidor"

        # Caja de texto con scroll para mostrar el ranking formateado en HTML
        pygame_gui.elements.UITextBox(
            html_text=ranking_text,
            relative_rect=pygame.Rect(30, 80, panel_width - 60, panel_height - 160),
            manager=self.manager,
            container=self.ranking_panel
        )

        # Botón para cerrar la ventana — object_id nos permite identificarlo en el bucle de eventos
        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 2 - 75, panel_height - 60, 150, 40),
            text='CERRAR',
            manager=self.manager,
            container=self.ranking_panel,
            object_id='#close_ranking'
        )

    def format_ranking(self, ranking):
        """Formatear el ranking como HTML para mostrarlo en el UITextBox"""
        html = "<font face='monospace' size=4>"
        # Cabecera de la tabla
        html += "<b>POS  USUARIO             PUNTOS      FECHA</b><br>"
        html += "─" * 50 + "<br>"

        for i, entry in enumerate(ranking, 1):
            # Truncamos el nombre a 15 caracteres y lo rellenamos con espacios para alinear
            username = entry['username'][:15].ljust(15)
            # Alineamos el score a la derecha con 8 caracteres
            score = str(entry['score']).rjust(8)
            # Nos quedamos solo con la fecha, quitando la hora
            date = entry['date'].split()[0] if ' ' in entry['date'] else entry['date']

            # Los tres primeros puestos tienen colores especiales
            if i == 1:
                color = "#FFD700"  # oro
            elif i == 2:
                color = "#C0C0C0"  # plata
            elif i == 3:
                color = "#CD7F32"  # bronce
            else:
                color = "#FFFFFF"  # resto en blanco

            html += f"<font color='{color}'>{str(i).rjust(2)}   {username}  {score}   {date}</font><br>"

        html += "</font>"
        return html

    def close_ranking(self):
        """Cerrar la ventana de ranking"""
        if self.ranking_panel:
            # kill() elimina el panel y todos sus elementos hijos de la memoria
            self.ranking_panel.kill()
            self.ranking_panel = None
            # Reseteamos el flag para poder abrir la ventana de nuevo si hace falta
            self.showing_ranking = False

    def show_instructions(self):
        """Mostrar instrucciones del juego en una ventana emergente"""
        if self.showing_instructions:
            return

        self.showing_instructions = True

        panel_width = 600
        panel_height = 550
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        self.instructions_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(50, 20, panel_width - 100, 40),
            text='INSTRUCCIONES',
            manager=self.manager,
            container=self.instructions_panel
        )

        # Contenido en HTML — pygame_gui soporta un subconjunto básico de HTML
        # usamos etiquetas font para cambiar colores y tamaños
        instructions_text = """
        <font size=3>
        <b>OBJETIVO:</b><br>
        Completa líneas horizontales para sumar puntos.
        ¡No dejes que las piezas lleguen arriba!<br><br>
        
        <b>CONTROLES:</b><br>
        <font color='#00FFFF'>IZQUIERDA/DERECHA</font> Mover pieza izquierda/derecha<br>
        <font color='#00FFFF'>ABAJO</font> Bajar pieza más rápido<br>
        <font color='#00FFFF'>ARRIBA</font> Rotar pieza<br>
        <font color='#00FFFF'>ESPACIO</font> Caída rápida instantánea<br>
        <font color='#00FFFF'>R</font> Reiniciar partida (tras Game Over)<br>
        <font color='#00FFFF'>ESC</font> Salir al menú<br><br>
        
        <b>PUNTUACIÓN:</b><br>
        • 1 línea = 100 puntos<br>
        • 2 líneas = 400 puntos<br>
        • 3 líneas = 900 puntos<br>
        • 4 líneas = 1600 puntos (¡TETRIS!)<br><br>
        
        <b>PIEZAS:</b><br>
        <font color='#00FFFF'>I</font> <font color='#FFFF00'>O</font> <font color='#FF00FF'>T</font> 
        <font color='#00FF00'>S</font> <font color='#FF0000'>Z</font> <font color='#0000FF'>J</font> 
        <font color='#FFA500'>L</font><br><br>
        
        ¡Buena suerte!
        </font>
        """

        pygame_gui.elements.UITextBox(
            html_text=instructions_text,
            relative_rect=pygame.Rect(30, 80, panel_width - 60, panel_height - 160),
            manager=self.manager,
            container=self.instructions_panel
        )

        pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_width // 2 - 75, panel_height - 60, 150, 40),
            text='CERRAR',
            manager=self.manager,
            container=self.instructions_panel,
            object_id='#close_instructions'
        )

    def close_instructions(self):
        """Cerrar la ventana de instrucciones"""
        if self.instructions_panel:
            self.instructions_panel.kill()
            self.instructions_panel = None
            self.showing_instructions = False