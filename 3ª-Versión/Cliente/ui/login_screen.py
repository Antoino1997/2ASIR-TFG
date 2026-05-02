# ui/login_screen.py

# pygame es la librería principal para gráficos y eventos
import pygame
# pygame_gui nos da componentes de interfaz ya hechos: botones, campos de texto, etiquetas
import pygame_gui
# Importamos todas las constantes de configuración (colores, tamaños, etc.)
from config import *

class LoginScreen:
    def __init__(self, screen, api_client):
        # Guardamos la pantalla y el cliente API para usarlos en los métodos
        self.screen = screen
        self.api_client = api_client

        # Obtenemos el tamaño real de la ventana para calcular posiciones
        screen_width, screen_height = screen.get_size()
        # El manager de pygame_gui gestiona todos los elementos de la interfaz
        # necesita saber el tamaño de la ventana para posicionar los elementos correctamente
        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        # Dimensiones del panel central donde van los campos de login
        panel_width = 400
        panel_height = 350
        # Calculamos la posición para que el panel quede centrado en la ventana
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        # Etiqueta del título — la ponemos 60px por encima del panel
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(panel_x, panel_y - 60, panel_width, 50),
            text='TETRIS - Login',
            manager=self.manager
        )

        # Campo de texto para el nombre de usuario
        # placeholder_text es el texto gris que aparece cuando está vacío
        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 50, panel_width - 100, 40),
            manager=self.manager,
            placeholder_text='Usuario'
        )

        # Campo de texto para la contraseña
        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 110, panel_width - 100, 40),
            manager=self.manager,
            placeholder_text='Contraseña'
        )
        # Ocultamos el texto para que aparezcan asteriscos en vez de los caracteres reales
        self.password_input.set_text_hidden(True)

        # Botón de login — a la izquierda
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 170, 140, 40),
            text='Entrar',
            manager=self.manager
        )

        # Botón de registro — a la derecha del botón de login
        self.register_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(panel_x + 210, panel_y + 170, 140, 40),
            text='Registrarse',
            manager=self.manager
        )

        # Etiqueta para mostrar mensajes de error o confirmación al usuario
        # empieza vacía y se rellena según lo que ocurra
        self.message_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(panel_x + 50, panel_y + 230, panel_width - 100, 50),
            text='',
            manager=self.manager
        )

    def run(self):
        """Ejecutar la pantalla de login"""
        clock = pygame.time.Clock()
        running = True

        while running:
            # time_delta es el tiempo en segundos desde el último frame
            # pygame_gui lo necesita para animar sus elementos correctamente
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                # Si el usuario cierra la ventana devolvemos None para que main lo gestione
                if event.type == pygame.QUIT:
                    return None, None

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        # Recogemos lo que ha escrito el usuario en los campos
                        username = self.username_input.get_text()
                        password = self.password_input.get_text()

                        if username and password:
                            # Enviamos las credenciales al servidor a través del api_client
                            success, message = self.api_client.login(username, password)
                            if success:
                                # Login correcto — devolvemos True y el nombre de usuario
                                # main.py usará estos valores para pasar al menú principal
                                return True, username
                            else:
                                # Login fallido — mostramos el error que devuelve el servidor
                                self.message_label.set_text(message)
                        else:
                            # El usuario dejó algún campo vacío
                            self.message_label.set_text("Completa todos los campos")

                    elif event.ui_element == self.register_button:
                        username = self.username_input.get_text()
                        password = self.password_input.get_text()

                        if username and password:
                            # Intentamos registrar el usuario en el servidor
                            success, message = self.api_client.register(username, password)
                            # Mostramos el mensaje del servidor (éxito o error)
                            self.message_label.set_text(message)
                            if success:
                                # Si el registro fue bien limpiamos los campos
                                # para que el usuario pueda hacer login a continuación
                                self.username_input.set_text("")
                                self.password_input.set_text("")
                        else:
                            self.message_label.set_text("Completa todos los campos")

                # Pasamos el evento al manager para que pygame_gui lo procese
                # sin esta línea los botones y campos de texto no funcionarían
                self.manager.process_events(event)

            # Actualizamos el estado interno de pygame_gui (animaciones, hover, etc.)
            self.manager.update(time_delta)

            # Pintamos el fondo negro antes de dibujar la interfaz
            # sin esto los frames anteriores se quedarían visible debajo
            self.screen.fill(BLACK)
            # Dibujamos todos los elementos de la interfaz sobre el fondo
            self.manager.draw_ui(self.screen)

            # Mostramos el frame en pantalla
            pygame.display.flip()

        return None, None