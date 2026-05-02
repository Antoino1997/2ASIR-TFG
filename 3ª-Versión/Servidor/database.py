# servidor/database.py

# sqlite3 es la librería que viene con Python para manejar bases de datos SQLite
import sqlite3
# os lo usamos para comprobar si existen carpetas y crearlas si hace falta
import os
# contextmanager nos permite crear el "with get_db()" que garantiza cerrar la conexión siempre
from contextlib import contextmanager
# Importamos nuestra configuración para saber dónde está el fichero de la base de datos
from config import Config

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""

    # Sacamos la carpeta donde debería estar el fichero .db (por ejemplo /app/data)
    db_dir = os.path.dirname(Config.DATABASE)
    # Si la carpeta no existe, la creamos — sin esto SQLite daría error al intentar crear el fichero
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Abrimos la conexión — si el fichero .db no existe, SQLite lo crea automáticamente
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # Creamos la tabla de usuarios solo si no existe ya
    # AUTOINCREMENT hace que el id se asigne solo y vaya subiendo
    # UNIQUE en username impide que dos usuarios tengan el mismo nombre
    # NOT NULL obliga a que esos campos siempre tengan valor
    # DEFAULT CURRENT_TIMESTAMP guarda automáticamente la fecha y hora de creación
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        username TEXT UNIQUE NOT NULL,
                                                        password_hash TEXT NOT NULL,
                                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')

    # Creamos la tabla de puntuaciones solo si no existe ya
    # FOREIGN KEY vincula cada puntuación con el usuario que la consiguió
    # Si intentas insertar un user_id que no existe en users, SQLite lo rechaza
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS scores (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         user_id INTEGER NOT NULL,
                                                         score INTEGER NOT NULL,
                                                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                         FOREIGN KEY (user_id) REFERENCES users(id)
                       )
                   ''')

    # Creamos un índice sobre la columna score ordenado de mayor a menor
    # Un índice es como el índice de un libro — permite encontrar datos mucho más rápido
    # sin tener que recorrer toda la tabla fila a fila
    cursor.execute('''
                   CREATE INDEX IF NOT EXISTS idx_scores_score
                       ON scores(score DESC)
                   ''')

    # Confirmamos todos los cambios para que se escriban en el fichero
    conn.commit()
    # Cerramos la conexión — aquí sí lo hacemos manual porque init_db es especial
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# El decorador @contextmanager convierte esta función en un "with"
# Esto garantiza que la conexión se cierra siempre, aunque ocurra un error
@contextmanager
def get_db():
    """Context manager para conexiones a la base de datos"""
    # Abrimos la conexión con la base de datos
    conn = sqlite3.connect(Config.DATABASE)
    # row_factory hace que las filas se comporten como diccionarios
    # así podemos hacer fila["username"] en vez de tener que recordar que username es la columna 0
    conn.row_factory = sqlite3.Row
    try:
        # Cedemos la conexión al bloque "with" para que haga su trabajo
        yield conn
    finally:
        # Esto se ejecuta SIEMPRE al salir del "with", haya error o no
        conn.close()

def get_user_by_username(username):
    """Obtener usuario por nombre de usuario"""
    # Abrimos conexión mediante el contextmanager — se cerrará sola al salir del with
    with get_db() as conn:
        cursor = conn.cursor()
        # El ? es un placeholder — nunca concatenamos strings en SQL para evitar inyección SQL
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        # fetchone devuelve una sola fila o None si no encuentra nada
        return cursor.fetchone()

def create_user(username, password_hash):
    """Crear un nuevo usuario"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # Insertamos el nuevo usuario con su contraseña ya encriptada
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            # Confirmamos la inserción para que se guarde en el fichero
            conn.commit()
            # lastrowid nos da el id que se le asignó automáticamente al nuevo usuario
            return True, cursor.lastrowid
        except sqlite3.IntegrityError:
            # IntegrityError ocurre cuando intentamos insertar un username que ya existe
            # gracias al UNIQUE que definimos en la tabla
            return False, None

def save_score(user_id, score):
    """Guardar una puntuación"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Insertamos la puntuación vinculada al usuario que la consiguió
        cursor.execute(
            'INSERT INTO scores (user_id, score) VALUES (?, ?)',
            (user_id, score)
        )
        # Confirmamos para que se guarde
        conn.commit()
        # Devolvemos el id de la puntuación recién guardada
        return cursor.lastrowid

def get_top_scores(limit=10):
    """Obtener las mejores puntuaciones"""
    with get_db() as conn:
        cursor = conn.cursor()
        # JOIN une las dos tablas para poder mostrar el nombre del usuario junto a su puntuación
        # sin el JOIN solo tendríamos el user_id, no el nombre
        # ORDER BY score DESC ordena de mayor a menor puntuación
        # LIMIT restringe cuántos resultados devolvemos
        cursor.execute('''
                       SELECT u.username, s.score, s.created_at
                       FROM scores s
                                JOIN users u ON s.user_id = u.id
                       ORDER BY s.score DESC
                           LIMIT ?
                       ''', (limit,))
        # fetchall devuelve todas las filas que coinciden con la consulta
        return cursor.fetchall()

def get_user_ranking_position(user_id, score):
    """Obtener la posición del usuario en el ranking"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Contamos cuántas puntuaciones hay mejores que la nuestra y le sumamos 1
        # si hay 4 puntuaciones mejores, estamos en posición 5
        # es más eficiente que traer el ranking completo y buscar nuestra posición en Python
        cursor.execute('''
                       SELECT COUNT(*) + 1 as position
                       FROM scores
                       WHERE score > ?
                       ''', (score,))
        result = cursor.fetchone()
        # Si hay resultado devolvemos la posición, si no devolvemos None
        return result[0] if result else None