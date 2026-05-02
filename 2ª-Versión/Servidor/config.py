# servidor/config.py
class Config:
    # Base de datos SQLite (para testing local)
    DATABASE = 'tetris.db'

    # Clave secreta para JWT
    SECRET_KEY = 'tu-clave-secreta-super-segura-cambiar-en-produccion'

    # Configuración Flask
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000