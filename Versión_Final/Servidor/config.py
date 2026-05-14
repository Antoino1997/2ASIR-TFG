# servidor/config.py
class Config:
    # Base de datos SQLite (para testing local)
    DATABASE = '/app/data/tetris.db'

    # Clave secreta para JWT
    SECRET_KEY = 'tu-clave-secreta-super-segura-cambiar-en-produccion'

    # Configuración Flask
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
