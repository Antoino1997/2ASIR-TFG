# servidor/app.py

# Importamos Flask y las herramientas que necesitamos para manejar peticiones y respuestas
from flask import Flask, request, jsonify, render_template
# CORS permite que el cliente Pygame (que está en otra máquina/puerto) pueda hablar con este servidor
from flask_cors import CORS
# bcrypt es la librería que usamos para encriptar contraseñas de forma segura
import bcrypt
# jwt nos permite crear tokens de sesión para que el usuario no tenga que loguearse en cada petición
import jwt
# datetime lo usamos para calcular cuándo expira el token
from datetime import datetime, timedelta
# Importamos nuestra configuración (puerto, clave secreta, etc.)
from config import Config
# Importamos nuestro módulo de base de datos con todas las funciones de consulta
import database

# Creamos la aplicación Flask
app = Flask(__name__)
# Le pasamos la configuración que tenemos en Config (puerto, debug, etc.)
app.config.from_object(Config)
# Activamos CORS para que el cliente pueda conectarse desde cualquier origen
CORS(app)

# Al arrancar el servidor, inicializamos la base de datos (crea las tablas si no existen)
database.init_db()

def create_token(user_id):
    """Crear un token JWT"""
    # El token contiene el id del usuario y una fecha de expiración de 7 días
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)  # el token caduca en 7 días
    }
    # Firmamos el token con nuestra clave secreta para que no pueda ser falsificado
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verificar y decodificar un token JWT"""
    try:
        # Intentamos decodificar el token con nuestra clave secreta
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        # Si es válido, devolvemos el id del usuario que contiene
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # El token existe pero ha caducado
        return None
    except jwt.InvalidTokenError:
        # El token no es válido o está manipulado
        return None

# Ruta principal — simplemente confirma que el servidor está vivo
@app.route('/')
def index():
    """Página principal"""
    return '''
    <h1>Tetris Server</h1>
    <p>Servidor funcionando correctamente</p>
    <ul>
        <li><a href="/ranking">Ver Ranking</a></li>
        <li><a href="/api/ranking">API Ranking (JSON)</a></li>
    </ul>
    '''

# Ruta para registrar un nuevo usuario, solo acepta peticiones POST
@app.route('/api/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    try:
        # Cogemos los datos que nos manda el cliente en formato JSON
        data = request.json
        # Sacamos el usuario y le quitamos espacios en blanco al principio y al final
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Comprobamos que no vengan vacíos
        if not username or not password:
            return jsonify({'success': False, 'error': 'Usuario y contraseña requeridos'}), 400

        # El nombre de usuario debe tener al menos 3 caracteres
        if len(username) < 3:
            return jsonify({'success': False, 'error': 'El usuario debe tener al menos 3 caracteres'}), 400

        # La contraseña debe tener al menos 4 caracteres
        if len(password) < 4:
            return jsonify({'success': False, 'error': 'La contraseña debe tener al menos 4 caracteres'}), 400

        # Encriptamos la contraseña antes de guardarla — nunca guardamos contraseñas en texto plano
        # gensalt() genera una "sal" aleatoria que hace que dos contraseñas iguales tengan hashes distintos
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Intentamos crear el usuario en la base de datos
        success, user_id = database.create_user(username, password_hash)

        if success:
            # Todo fue bien
            return jsonify({
                'success': True,
                'message': 'Usuario registrado correctamente'
            }), 200
        else:
            # Si llegamos aquí es porque el usuario ya existe (IntegrityError en la BD)
            return jsonify({
                'success': False,
                'error': 'El usuario ya existe'
            }), 400

    except Exception as e:
        # Capturamos cualquier error inesperado para que el servidor no se caiga
        print(f"Error en register: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

# Ruta para iniciar sesión, solo acepta peticiones POST
@app.route('/api/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Comprobamos que no vengan vacíos
        if not username or not password:
            return jsonify({'success': False, 'error': 'Usuario y contraseña requeridos'}), 400

        # Buscamos el usuario en la base de datos
        user = database.get_user_by_username(username)

        if not user:
            # No decimos "el usuario no existe" por seguridad — así no revelamos qué usuarios existen
            return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401

        # Comparamos la contraseña que nos manda con el hash guardado en la BD
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Contraseña correcta — creamos el token de sesión
            token = create_token(user['id'])
            return jsonify({
                'success': True,
                'token': token,        # El cliente guardará este token para futuras peticiones
                'user_id': user['id'],
                'username': user['username']
            }), 200
        else:
            # Contraseña incorrecta
            return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401

    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

# Ruta para guardar una puntuación, solo acepta peticiones POST
@app.route('/api/score', methods=['POST'])
def save_score():
    """Guardar una puntuación"""
    try:
        # Miramos si viene el header de autorización con el token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            # Si no hay token, rechazamos la petición — no puedes guardar puntuación sin estar logueado
            return jsonify({'success': False, 'error': 'Token no proporcionado'}), 401

        # El header viene como "Bearer el_token_aqui" — nos quedamos solo con el token
        token = auth_header.split(' ')[1]
        # Verificamos el token y obtenemos el id del usuario
        user_id = verify_token(token)

        if not user_id:
            # El token no es válido o ha caducado
            return jsonify({'success': False, 'error': 'Token inválido o expirado'}), 401

        data = request.json
        score = data.get('score', 0)

        # Validamos que la puntuación sea un número entero positivo
        if not isinstance(score, int) or score < 0:
            return jsonify({'success': False, 'error': 'Puntuación inválida'}), 400

        # Guardamos la puntuación en la base de datos
        score_id = database.save_score(user_id, score)

        # Calculamos en qué posición del ranking queda esta puntuación
        position = database.get_user_ranking_position(user_id, score)

        return jsonify({
            'success': True,
            'score_id': score_id,
            'ranking_position': position  # le decimos al cliente en qué posición ha quedado
        }), 200

    except Exception as e:
        print(f"Error en save_score: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

# Ruta para obtener el ranking en formato JSON — lo usa el cliente Pygame
@app.route('/api/ranking')
def get_ranking():
    """Obtener el ranking (API JSON)"""
    try:
        # Permite pedir un número concreto de resultados, por defecto 10
        limit = request.args.get('limit', 10, type=int)
        # Ponemos un tope de 100 para que nadie pida millones de registros
        limit = min(limit, 100)

        scores = database.get_top_scores(limit)

        # Convertimos cada fila de la BD a un diccionario limpio para el JSON
        ranking = []
        for score in scores:
            ranking.append({
                'username': score['username'],
                'score': score['score'],
                'date': score['created_at']
            })

        return jsonify({'ranking': ranking}), 200

    except Exception as e:
        print(f"Error en get_ranking: {e}")
        # Si algo falla devolvemos un ranking vacío en vez de un error — el cliente lo maneja mejor
        return jsonify({'ranking': []}), 500

# Ruta para ver el ranking en el navegador como página web
@app.route('/ranking')
def ranking_page():
    """Página web del ranking"""
    try:
        # Cogemos el top 10 y lo pasamos a la plantilla HTML
        scores = database.get_top_scores(10)
        return render_template('ranking.html', scores=scores)
    except Exception as e:
        print(f"Error en ranking_page: {e}")
        return "Error al cargar el ranking", 500

# Punto de entrada — solo se ejecuta si lanzamos el fichero directamente, no si lo importa otro módulo
if __name__ == '__main__':
    print("Iniciando servidor Tetris...")
    print(f"Servidor corriendo en http://{Config.HOST}:{Config.PORT}")
    print(f"Ranking disponible en http://localhost:{Config.PORT}/ranking")
    # Arrancamos el servidor con la configuración de config.py
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)