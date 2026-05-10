# main.py
import pygame
import sys
from config import *
from api_client import APIClient
from ui.login_screen import LoginScreen
from ui.menu import Menu
from game.tetris import Tetris
from game.renderer import Renderer

def main():
    # Inicializar Pygame
    pygame.init()

    # Cliente API
    api_client = APIClient()

    # Pantalla de login (puede ser más pequeña)
    login_screen_size = (600, 500)
    screen = pygame.display.set_mode(login_screen_size)
    pygame.display.set_caption("Tetris - Login")

    # Pantalla de login
    login_screen = LoginScreen(screen, api_client)
    success, username = login_screen.run()

    if not success:
        pygame.quit()
        sys.exit()

    # RECREAR la ventana con el tamaño correcto para el juego
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Bucle principal del programa
    while True:
        # Mostrar menú
        menu = Menu(screen, api_client, username)
        action = menu.run()

        if action == 'exit':
            break
        elif action == 'play':
            # Iniciar juego
            game_result = run_game(screen, api_client, username, clock)
            if game_result == 'exit':
                break

    pygame.quit()
    sys.exit()

def run_game(screen, api_client, username, clock):
    """Ejecutar una partida de Tetris"""
    tetris = Tetris(api_client)
    renderer = Renderer(screen)

    running = True
    while running:
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'

            if event.type == pygame.KEYDOWN:
                if not tetris.game_over:
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
                        return 'menu'  # Volver al menú
                else:
                    if event.key == pygame.K_r:
                        tetris.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return 'menu'  # Volver al menú

        # Actualizar
        tetris.update()

        # Dibujar
        screen.fill(BLACK)
        renderer.draw_board(tetris.board)
        renderer.draw_piece(tetris.current_piece)
        renderer.draw_next_piece(tetris.next_piece)
        renderer.draw_info(tetris, username)

        if tetris.game_over:
            renderer.draw_game_over(tetris.score)

        pygame.display.flip()

    return 'menu'

if __name__ == "__main__":
    main()