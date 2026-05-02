# api_client.py

# requests es la librería que usamos para hacer peticiones HTTP al servidor Flask
import requests
# json viene incluido en Python, aunque aquí no se usa directamente
# requests ya maneja la conversión a JSON internamente
import json
# Importamos la URL del servidor desde config.py para no tenerla hardcodeada aquí
from config import SERVER_URL

class APIClient:
    def __init__(self):
        # El token JWT que nos da el servidor al hacer login
        # Empieza vacío porque todavía no hemos iniciado sesión
        self.token = None
        # El id numérico del usuario en la base de datos
        self.user_id = None
        # El nombre de usuario con el que se ha iniciado sesión
        self.username = None

    def register(self, username, password):
        """Registrar un nuevo usuario"""
        try:
            # Hacemos una petición POST al endpoint de registro
            # json= convierte automáticamente el diccionario a JSON y añade el header Content-Type
            # timeout=5 significa que si el servidor no responde en 5 segundos, lanzamos error
            response = requests.post(
                f"{SERVER_URL}/api/register",
                json={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                # Convertimos la respuesta JSON a diccionario Python
                data = response.json()
                # Si el servidor dice que fue bien, devolvemos True y el mensaje
                return data.get("success", False), data.get("message", "Registrado correctamente")
            else:
                # El servidor respondió pero con un error (400, 500, etc.)
                error_data = response.json()
                return False, error_data.get("error", "Error al registrar")

        except requests.exceptions.ConnectionError:
            # El servidor no está encendido o no es accesible desde esta red
            return False, "No se pudo conectar al servidor"
        except Exception as e:
            # Cualquier otro error inesperado
            return False, f"Error: {str(e)}"

    def login(self, username, password):
        """Iniciar sesión"""
        try:
            # Enviamos las credenciales al endpoint de login
            response = requests.post(
                f"{SERVER_URL}/api/login",
                json={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                # Guardamos el token JWT para usarlo en futuras peticiones autenticadas
                # sin este token no podemos guardar puntuaciones
                self.token = data["token"]
                # Guardamos el id y nombre de usuario para tenerlos disponibles en el cliente
                self.user_id = data["user_id"]
                self.username = username
                return True, "Login exitoso"
            else:
                # El servidor respondió pero las credenciales son incorrectas
                return False, "Usuario o contraseña incorrectos"

        except requests.exceptions.ConnectionError:
            return False, "No se pudo conectar al servidor"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def save_score(self, score):
        """Guardar puntuación"""
        # Si no tenemos token es que no se ha hecho login — no tiene sentido continuar
        if not self.token:
            return False, "No has iniciado sesión"

        try:
            # Esta petición necesita autenticación, así que añadimos el token en el header
            # El formato "Bearer token" es el estándar para autenticación JWT
            response = requests.post(
                f"{SERVER_URL}/api/score",
                headers={"Authorization": f"Bearer {self.token}"},
                json={"score": score},
                timeout=5
            )

            if response.status_code == 200:
                # La puntuación se guardó correctamente en la base de datos
                data = response.json()
                return True, "Puntuación guardada"
            else:
                return False, "Error al guardar puntuación"

        except requests.exceptions.ConnectionError:
            return False, "No se pudo conectar al servidor"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_ranking(self, limit=10):
        """Obtener el ranking"""
        try:
            # Esta petición es GET y no necesita autenticación — cualquiera puede ver el ranking
            # limit lo pasamos como parámetro en la URL: /api/ranking?limit=10
            response = requests.get(
                f"{SERVER_URL}/api/ranking?limit={limit}",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                # Devolvemos la lista de puntuaciones que viene dentro de la clave "ranking"
                return True, data["ranking"]
            else:
                # Si algo falla devolvemos lista vacía para que el cliente lo maneje bien
                return False, []

        except requests.exceptions.ConnectionError:
            # Sin conexión devolvemos lista vacía — el menú mostrará "no hay puntuaciones"
            return False, []
        except Exception as e:
            return False, []