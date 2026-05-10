<div align="center">
  <h1>TFG - Antonio Pérez Galán</h1>
  <p>Desarrollo de un videojuego en red con Python, Flask y Docker</p>
</div>

## Índice
- [Introducción](#introducción)
- [Arquitectura y Tecnologías Usadas](#arquitectura-y-tecnologías-usadas)
- [Explicación Tecnologías y Alternativas](#explicación-tecnologías-y-alternativas)
- [Estructura de Datos](#estructura-de-datos)
- [Estructura del Proyecto (Carpetas)](#estructura-del-proyecto)
- [Flujo de Comunicación](#flujo-de-comunicación)
- [Historial de Versiones](#historial-de-versiones)
- [Docker y Distribución](#docker-y-distribución)

## Introducción

Este Trabajo de Fin de Grado presenta el desarrollo de un sistema cliente-servidor basado en Python cuyo objetivo es gestionar y registrar puntuaciones de un videojuego tipo Tetris. El sistema se compone de un servidor web implementado con Flask, que expone una API para la autenticación de usuarios y el almacenamiento de puntuaciones, haciendo uso de tecnologías como Flask-CORS, bcrypt y PyJWT para garantizar la seguridad y la comunicación entre servicios.

Por otro lado, se ha desarrollado un cliente de escritorio del juego Tetris utilizando Pygame, que permite a los usuarios iniciar sesión, jugar y enviar sus puntuaciones al servidor mediante peticiones HTTP con la librería Requests, incorporando además una interfaz gráfica mediante pygame-gui. El servidor complementa esta funcionalidad con una página web que muestra el ranking global de los diez mejores jugadores, apoyado en una base de datos que gestiona la información de usuarios y resultados.

En conjunto, este proyecto integra desarrollo de aplicaciones, diseño de APIs y gestión de datos, ofreciendo una solución completa para la interacción entre un videojuego cliente y un servicio backend.

## Arquitectura y Tecnologías Usadas

### Arquitectura

<img width="1920" height="1080" alt="Mapa Concentual 1" src="https://github.com/user-attachments/assets/557b5d3b-e898-43c6-86f9-611801478149" />

### Tecnologías Usadas
#### Cliente
- Lenguaje -> Python
- Framework UI -> Pygame (Ventana del juego)
- Framework GUI -> pygame_gui (Menús y login)
- HTTP Client -> Requests (Peticiones al servidor)
- Sistema operativo -> Cualquiera

#### Servidor
- Lenguaje -> Python
- Framework Web -> Flask
- CORS -> Flask-CORS (Permitir peticiones cross-origin)
- Base de datos -> SQLite3
- Seguridad
  - Hashing -> bcrypt
  - Autenticación -> PyJWT
- Plantillas -> Jinja2 (Para la página web ranking.html)

#### Comunicación
- Protocolo -> HTTP / HTTPS
- Formato de datos -> JSON
- Autenticación -> JWT Bearer Tokens
- Puerto -> 5000 (Configurable)

## Explicación Tecnologías y Alternativas
### Python
Lenguaje de programación principal tanto para cliente como para servidor.
- Usado por:
  - Simplicidad
  - Multiplataforma
  - Ecosistema amplio (librerías)
  - Es lo que estoy estudiando de optativa.
- Alternativas:
  - JavaScript (Node.js)
    - Ventaja(s) -> Frontend y backend con el mismo lenguaje.
    - Desventaja(s) -> Menos apropiado para juegos de escritorio.
  - Java
    - Ventaja(s) -> Muy robusto, multiplataforma.
    - Desventaja(s) -> Curva de aprendizaje mayor.
  - C++
    - Ventaja(s) -> El más rápido actualmente.
    - Desventaja(s) -> Complejidad excesiva.
  - C#
    - Ventaja(s) -> Excelentee para juegos (Unity)
    - Desventaja(s) -> Menos portable (.net y NuGet) y ecosistema cerrado.
- Conclusión:
  - Lo he usado ya que es una de mis asignaturas y además es fácil de usar y desarrollar.
 
### Pygame
Framework para crear la interfaz gráfica del juego (ventana, piezas, tablero y renderizado).
- Usado por:
  - Específico para el desarrollo de videojuegos 2D.
  - Completo, ya que maneja los gráficos, los eventos, los sonidos y las colisiones.
  - Gran comunidad y sin fin de tutoriales.
  - Gratuito y open source.
- Alternativas:
  - TKinter
    - Ventaja(s) -> Viene con python por defecto.
    - Desventaja(s) -> Limitado para juegos, menos visual.
  - PyQT / PySide
    - Ventaja(s) -> Interfaces profesionales.
    - Desventaja(s) -> Demasiado para mi juego, usa licencias.
  - Arcade
    - Ventaja(s) -> Más moderno que Pygame
    - Desventaja(s) -> Al ser más nuevo hay menos documentación.
  - Kivy
    - Ventaja(s) -> Multiplataforma y soporte para móviles.
    - Desventaja(s) -> Más complejo.
  - Unity + Python
    - Ventaja(s) -> Motor profesional.
    - Desventaja(s) -> Complejidad excesiva, curva de aprendizaje mayor.
- Conclusión:
  - Al estar buscando información sobre como hacer un juego sencillo he encontrado que Pygame es el estándar en juegos 2D en Python por su simplicidad y curva de aprendizaje muy buena para principiantes como yo.
 
### pygame_gui
Librería de interfaz de usuario (botones, campos de texto, ventanas) construida sobre Pygame.
- Usado por:
  - Integración perfecta para Pygame.
  - Componentes listos sin programarlos desde cero.
  - Gestión de eventos automática.
- Alternativas:
  - Pygame nativo
    - Ventaja(s) -> Sin dependencias extra.
    - Desventaja(s) -> Hay que programar cada botón manualmente.
  - TKinter embebido.
    - Ventaja(s) -> Más componentes.
    - Desventaja(s) -> Mezclar frameworks es complicado.
  - Pygame Menu
    - Ventaja(s) -> Similar a pygame_gui.
    - Desventaja(s) -> Menos flexible.
- Conclusión:
  - Esta librería me ahorra tiempo de desarrollo y proporciona una interfaz profesional con mínimo esfuerzo.

### FLASK
Microframework web para crear la API REST del servidor.
- Usado por:
  - Minimalista.
  - Flexible, ya que puedo agregar solo las extensiones que necesito (CORS, JWT).
  - Muy fácil de entender y una API simple e intuitiva.
  - Muy bien documentado.
  - Ideal para API REST.
- Alternativas:
  - Django
    - Ventaja(s) -> Framework completo (admin, ORM, etc...).
    - Desventaja(s) -> Demasiado pesado para la API que quiero diseñar.
  - FastAPI
    - Ventaja(s) -> Más moderno, async, documentación automática.
    - Desventaja(s) -> Está más verde y es innecesario.
  - Express.js
    - Ventaja(s) -> Muy popular y con un ecosistema enorme.
    - Desventaja(s) -> Necesita Node.js
  - ASP.NET Core
    - Ventaja(s) -> Muy robusto y corporativo.
    - Desventaja(s) -> Ecosistema Microsoft y más complejo.
- Conclusión:
  - He elegido FLASK ya que es perfecto para las APIs pequeñas como la que quiero diseñar. Además es simple y ligero ya que solo instalo lo necesario.

### SQLite
Base de datos relacional ligeral que será la encargada de guardar los usuarios y las puntuaciones en un archivo.
- Usado por:
  - Sin instalación ya que viene integrado con Python.
  - Sin servidor (no requiere un proceso separado).
  - Toda la base de datos en un único .db.
  - Portable ya que solo se tiene que copiar el archivvo .db.
  - SQL completo.
  - Rendimiento necesario para mi proyecto.
- Alternativas:
  - MySQL
    - Ventaja(s) -> Más robusto y mejor para alta concurrencia.
    - Desventaja(s) -> Requiere instalación y configuración.
  - PostgreSQL
    - Ventaja(s) -> Características más avanzadas.
    - Desventaja(s) -> Complejidad innecesaria y requiere servidor.
  - MongoDB
    - Ventaja(s) -> NoSQL y flexible.
    - Desventaja(s) -> Demasiado para datos relacionales simples.
  - Archivos JSON
    - Ventaja(s) -> Muy simple.
    - Desventaja(s) -> Sin integridad y sin consultas complejas.
- Conclusión:
  - SQLite es suficiente ya que mi aplicación va a ser pequeña y es cero configuración. Además para traspasar la base de datos solo tengo que moer el archivo .db.

### bcrypt
Algoritmo de hashingg para encriptar contraseñas de forma segura.
- Usado por:
  - Estándar de seguridad.
  - Lento a propósito (dificulta ataques de fuerza bruta).
  - Salto automático (cada contraseña tiene un hash único).
  - Unidireccional (imposible revertir el hash a la contraseña).
  - Resistente al tiempo.
- Alternativas:
  - Argon2
    - Ventaja(s) -> Más moderno.
    - Desventaja(s) -> Dependencias extra.
  - scrypt
    - Ventaja(s) -> Resistente a hardware especializado.
    - Desventaja(s) -> Más difícil de configurar.
  - PBKDF2
    - Ventaja(s) -> Estándar NIST (Instituto Nacional de Estándares y Tecnología).
    - Desventaja(s) -> Más lento que bcrypt.
  - MD5/SHA1
    - Ventaja(s) -> Muy rápido.
    - Desventaja(s) -> Inseguro.
- Conclusión:
  - He leído que encriptar las contraseñas es buena práctica y he estado leyendo que con dos líneas de código (encode / decode) puedo introducir este algoritmo en mi servidor.

### PyJWT (JSON Web Tokens)
Genera y valida tokens de autenticación que identifican usuarios entre peticiones.
- Usado por:
  - Stateless (el seridor no guarda sesiones).
  - Autocontenido (el token incluye toda la información necesaria).
  - Estándar Web (usado por Google, Facebook, Github, etc...).
  - Los tokens tienen fecha de caducidad (configurable).
  - Firmado (no se pueden falsificar sin la clave secreta).
- Alternativas:
  - Sesiones FLASK
    - Ventaja(s) -> Más simple, integrado.
    - Desventaja(s) -> Requiere base de datos / cookies.
  - OAuth 2.0
    - Ventaja(s) -> Estándar corporativo.
    - Desventaja(s) -> Complejidad excesiva para mi proyecto.
  - API Keys
    - Ventaja(s) -> Muy simple.
    - Desventaja(s) -> Menos seguro y los tokens / keys no expiran.
  - Cookies de sesión
    - Ventaja(s) -> Soportado nativamente.
    - Desventaja(s) -> Problemas con CORS.
- Conclusión:
  - Al principio me estuve informando de que si no introduces algo para que el servidor "recuerde" (sesiones) al quere hacer algo en el cliente que requiera de comunicación con el servidor (guardar puntuaciones, ver ranking, etc...) tendría que identificarme de nuevo. Por eso miré maneras de generar sesiones y encontré JWT que es muy fácil de aprender y es el estándar para API REST.

### requests
Librería de Python para hacer peticiones HTTP desde el cliente al servidor.
- Usado por:
  - API simple (es literalmente una línea de código).
  - Manejo automático (JSON, headers, cookies).
  - Es la librería HTTP más usada en Python.
  - Buena documentación con ejemplo claros.
  - Manejo de errores, timeouts y reintentos.
- Alternativas:
  - urllib
    - Ventaja(s) -> Es nativo de Python.
    - Desventaja(s) -> API más compleja y menos intuitia.
  - httpx
    - Ventaja(s) -> Async, HTTP/2
    - Desventaja(s) -> Innecesario para mi proyecto.
  - aiohttp
    - Ventaja(s) -> Async.
    - Desventaja(s) -> Demasiado complejo para mi proyecto.
- Conclusión:
  - Estuve mirando formas de comunicar el cliente y el servvidor, y requests fue una de las más recomendadas por su simplicidad a la hora de implementarse, por su automatización y por su amplia documentación. Además, al ser una librería de Python encaja perfectamente en mi proyecto.

### Flask - CORS
Permite que el cliente pueda hacer peticiones al servidor desde otro puerto o dominio.
- Usado por:
  - Sin CORS, el navegador bloquea peticiones entre dominios.
  - Con una línea de código se habilita.
  - Es muy configurable (lista blanca).
  - Es requerido por la política de seguridad de navegadores.
- Alternativas:
  - CORS manual
    - Ventaja(s) -> Sin dependencias.
    - Desventaja(s) -> Tedioso y propenso a errores si no se configura bien.
  - Proxy reverso
    - Ventaja(s) -> Solución a nivel infraestructura.
    - Desventaja(s) -> Más complejo, requiere Nginx / Apache.
- Conclusión:
  - Al hacer mi investigación sobre estándares, y aunque en mi proyecto no va a hacer nada, vi que CORS era requerido en caso de juntar dominios / subdominios u otros puertos. Como solo es una línea de código he decidido implementarlo.
- Ejemplo:
<img width="1920" height="1080" alt="Ejemplo CORS" src="https://github.com/user-attachments/assets/d615d768-7d0a-46b4-84da-0044eabb8950" />

## Estructura de Datos
### API Endpoints
  - POST /api/register
    - Request -> {username: string, password: string}
    - Response -> {success: bool, message: string}
  
  - POST /api/login
    - Request -> {username: string, password: string}
    - Response -> {success: bool, token: string, user_id: int}
  
  - POST /api/score
    - Headers -> {Authorization: "Bearer <token>"}
    - Request -> {score: int}
    - Response -> {success: bool, ranking_position: int}

  - GET /api/ranking?limit=10
    - Response -> {ranking: [{username, score, date}, ...]}

### Base de Datos
  - Tabla users
    - id (INTEGER PRIMARY KEY)
    - username (TEXT UNIQUE)
    - password_hash (TEXT)
    - created_at (TIMESTAMP)

  - Tabla scores
    - id (INTEGER PRIMARY KEY)
    - user_id (INTEGER FOREIGN KEY -> users.id)
    - created_at (TIMESTAMP)

### Seguridad
  - Contraseñas -> hasheadas con bcrypt
  - Autenticación -> JWT Tokens
  - Autorización -> Bearer tokens en headers

## Estructura del Proyecto
<img width="1920" height="1080" alt="Estructura Cliente" src="https://github.com/user-attachments/assets/cf9d7f14-d97b-4658-9e53-5095a3578a8e" />
<br/> <img width="1920" height="1080" alt="Esquema Servidor" src="https://github.com/user-attachments/assets/bb1f0689-f4a1-4112-871a-701bca5fa8e5" />

## Flujo de Comunicación
### Fase 1: Registro
<img width="1920" height="1080" alt="Flujo de comunicación Fase 1" src="https://github.com/user-attachments/assets/d19a1f62-805c-4af5-bdd1-490dfcb6775a" />

### Fase 2: Login
<img width="1920" height="1080" alt="Flujo de comunicación Fase 2" src="https://github.com/user-attachments/assets/69c1966e-8ff0-4741-88eb-89ff4e385f9c" />

### Fase 3: Jugar
<img width="1920" height="1080" alt="Flujo de comunicación Fase 3" src="https://github.com/user-attachments/assets/2ba497e3-e3df-4e12-9d65-79a23e3325ff" />

### Fase 4: Guardar Puntuación
<img width="1920" height="1080" alt="Flujo de comunicación Fase 4" src="https://github.com/user-attachments/assets/3c6705cd-d87a-4988-80b5-04f375b6bdd6" />

### Fase 5: Ver Ranking
<img width="1920" height="1080" alt="Flujo de comunicación Fase 5" src="https://github.com/user-attachments/assets/bdfdc2cb-1054-4d63-9107-2bbaecdbd00e" />

## Historial de Versiones

### v1.0 — Tetris Standalone + Inicio del Servidor
La primera versión del proyecto se centró en desarrollar el juego funcional de forma
completamente local, sin ninguna dependencia externa ni conexión de red.

**Cliente:**
- Implementación completa del juego Tetris en un único archivo (`tetris_standalone.py`)
- Toda la lógica en un solo fichero: piezas, tablero, renderizado y menú
- Las 7 piezas con sus rotaciones definidas mediante matrices
- Sistema de puntuación (100 puntos por línea, bonus por líneas múltiples)
- Menú principal con opciones de jugar, ver controles y salir
- Sin dependencias externas más allá de `pygame`

**Servidor:**
- Inicio del diseño de la API REST con Flask
- Definición de los endpoints básicos: `/api/register`, `/api/login`, `/api/score`, `/api/ranking`
- Estructura inicial de la base de datos SQLite con las tablas `users` y `scores`

**Dependencias:**
- pygame==2.5.2

---

### v2.0 — División de Responsabilidades + Servidor Completo
La segunda versión supuso una refactorización completa del cliente aplicando el principio
de separación de responsabilidades, y el desarrollo completo del servidor con todas sus
funcionalidades de seguridad y comunicación.

**Cliente:**
- Separación del código en módulos independientes:
  - `config.py` — constantes y configuración
  - `game/board.py` — lógica del tablero
  - `game/pieces.py` — definición y rotación de piezas
  - `game/tetris.py` — lógica principal del juego
  - `game/renderer.py` — renderizado y dibujado
  - `ui/login_screen.py` — pantalla de inicio de sesión
  - `ui/menu.py` — menú principal con ranking e instrucciones
  - `api_client.py` — comunicación HTTP con el servidor
- Incorporación de `pygame_gui` para los menús y pantalla de login
- Conexión con el servidor para login, registro y guardado de puntuaciones
- Visualización del ranking global descargado del servidor

**Servidor:**
- API REST completamente desarrollada con Flask
- Autenticación de usuarios con tokens JWT (caducidad de 7 días)
- Encriptación de contraseñas con bcrypt
- Base de datos SQLite con índice de rendimiento sobre puntuaciones
- Context manager para gestión segura de conexiones a la base de datos
- Página web del ranking en HTML con Jinja2 (`/ranking`)
- Habilitación de CORS con Flask-CORS

**Dependencias:**
- pygame==2.5.2
- requests==2.31.0
- pygame-gui==0.6.9
- flask
- flask-cors
- bcrypt
- pyjwt

---

### v3.0 — Servidor Dockerizado + Cliente Ejecutable
La tercera versión se centró en el despliegue y la distribución del proyecto,
haciendo que tanto el servidor como el cliente fueran fáciles de ejecutar en
cualquier máquina sin necesidad de instalar dependencias manualmente.

**Servidor:**
- Creación del `Dockerfile` para contenerizar el servidor Flask
- Creación del `docker-compose.yml` con volumen nombrado para persistencia de la base de datos
- Publicación de la imagen en Docker Hub (`jaceshadowninja/tetris-server:1.0`)
- El servidor arranca con un único comando: `docker compose up`

**Cliente:**
- Empaquetado del cliente Pygame como ejecutable `.exe` con PyInstaller
- El cliente puede ejecutarse en Windows sin tener Python instalado
- Distribución simplificada para el ordenador del profesor

**Dependencias servidor (imagen Docker):**
- flask
- flask-cors
- bcrypt
- pyjwt
- sqlite3

---

### v4.0 — Versión Final
La versión final se dedicó a la estabilización del proyecto, corrección de errores
detectados durante las pruebas y elaboración de la documentación completa.

**Corrección de errores:**
- Centrado correcto de los bloques decorativos en el menú principal
- Corrección de la indentación del método `draw_background()` en `menu.py`
- Eliminación del `RUN python -c "import database; database.init_db()"` del Dockerfile
  (la base de datos se inicializa en tiempo de ejecución, no durante la construcción de la imagen)
- Precarga de la fuente `fira_code` en `pygame_gui` para eliminar warnings en la pantalla de instrucciones
- Corrección del `docker-compose.yml`: sustitución de `build: .` por `image:` para usar
  la imagen publicada en Docker Hub

**Documentación:**
- Elaboración completa del `README.md` con introducción, arquitectura, tecnologías
  y alternativas, estructura de datos, estructura del proyecto y flujo de comunicación
- Comentado línea a línea de todos los ficheros del proyecto
- Historial de versiones

**Toques finales:**
- Rediseño de la página web del ranking con estética editorial (`ranking.html`)
- Ajuste de márgenes y dimensiones del panel de información del juego

## Docker y Distribución

### ¿Por qué Docker?

Durante el desarrollo del servidor surgió un problema clásico: el servidor funcionaba
perfectamente en mi ordenador, pero al intentar ejecutarlo en otro ordenador había que
instalar Python, Flask, bcrypt, y todas las dependencias manualmente, y cualquier
diferencia de versión podía romper el funcionamiento.

Docker soluciona esto empaquetando el servidor junto con todas sus dependencias en una
**imagen** — un paquete autocontenido que funciona igual en cualquier máquina que tenga
Docker instalado, independientemente del sistema operativo o de lo que tenga instalado.

---

### Conceptos Clave

- **Imagen** — la "plantilla" del servidor. Contiene el sistema operativo base, Python,
  todas las librerías y el código. Se construye una vez con `docker build` y se puede
  distribuir a cualquier máquina.

- **Contenedor** — una instancia en ejecución de la imagen. Es lo que realmente está
  corriendo cuando el servidor está activo. Se puede parar, reiniciar o eliminar sin
  afectar a la imagen.

- **Volumen** — mecanismo de persistencia de datos. Como los contenedores son efímeros
  (al eliminarlos pierden sus datos), el volumen guarda la base de datos SQLite fuera
  del contenedor para que sobreviva a reinicios y actualizaciones.

- **Docker Hub** — repositorio público de imágenes, equivalente a GitHub pero para
  imágenes Docker. Desde aquí el profesor puede descargar la imagen sin necesitar
  el código fuente.

---

### Dockerfile

El `Dockerfile` es el fichero que define cómo se construye la imagen del servidor:

```dockerfile
FROM python:3.11-slim                          # imagen base con Python 3.11

WORKDIR /app                                   # directorio de trabajo dentro del contenedor

RUN apt-get update && apt-get install -y \
    sqlite3 && \                               # instalamos sqlite3 para poder inspeccionar la BD
    rm -rf /var/lib/apt/lists/*                # limpiamos cache para reducir el tamaño de la imagen

COPY requirements.txt .                        # copiamos las dependencias
RUN pip install --no-cache-dir -r \
    requirements.txt                           # instalamos las dependencias

COPY . .                                       # copiamos todo el código del servidor

EXPOSE 5000                                    # indicamos que el servidor escucha en el puerto 5000

ENV FLASK_ENV=production                       # configuramos el entorno como producción
ENV PYTHONUNBUFFERED=1                         # los logs aparecen en tiempo real sin buffer

CMD ["python", "app.py"]                       # comando que arranca el servidor
```

---

### docker-compose.yml

El `docker-compose.yml` define cómo se arranca el contenedor con toda su configuración:

```yaml
version: '3.8'

name: tetris-server                            # nombre del proyecto en Docker Desktop

services:
  tetris-server:
    image: jaceshadowninja/tetris-server:1.0   # imagen descargada de Docker Hub
    container_name: tetris-server              # nombre del contenedor
    ports:
      - "5000:5000"                            # puerto del host : puerto del contenedor
    volumes:
      - tetris-data:/app/data                  # volumen nombrado para persistir la base de datos
    environment:
      - FLASK_ENV=production
      - DATABASE=/app/data/tetris.db           # ruta de la base de datos dentro del contenedor
    restart: unless-stopped                    # el contenedor se reinicia solo si se cae
    networks:
      - tetris-network

volumes:
  tetris-data:                                 # Docker gestiona el volumen internamente
    driver: local

networks:
  tetris-network:
    driver: bridge
```

Se eligió **volumen nombrado** en vez de bind mount (carpeta local) porque al mover
el proyecto a otro ordenador solo hace falta el `docker-compose.yml` — Docker crea
el volumen automáticamente sin necesidad de crear carpetas manualmente.

---

### Flujo de Despliegue

**En mi máquina (desarrollo):**
```bash
# 1. Construir la imagen con el Dockerfile
docker build -t jaceshadowninja/tetris-server:1.0 .

# 2. Subir la imagen a Docker Hub
docker login
docker push jaceshadowninja/tetris-server:1.0
```

**En el ordenador del profesor (exposición):**
```bash
# 1. Ir a la carpeta del servidor
cd ruta/Servidor

# 2. Descargar el proyecto
docker login
docker pull jaceshadowninja/tetris-server:1.0

# 3. Arrancar — Docker descarga la imagen automáticamente y arranca el contenedor
docker compose up
```

El servidor queda accesible en `http://localhost:5000` y el ranking en
`http://localhost:5000/ranking`.

---

### Inspeccionar la Base de Datos

Si durante la exposición se necesita ver el contenido de la base de datos:

```bash
# Entrar al contenedor
docker exec -it tetris-server bash

# Abrir la base de datos
sqlite3 /app/data/tetris.db

# Consultas útiles
.tables                    # ver todas las tablas
SELECT * FROM users;       # ver usuarios registrados
SELECT * FROM scores;      # ver puntuaciones guardadas
.quit                      # salir
```

---

### Ejecutable del Cliente (.exe)

#### ¿Por qué un ejecutable?

El cliente está desarrollado en Python, lo que significa que para ejecutarlo
normalmente hace falta tener Python instalado junto con todas sus dependencias
(`pygame`, `pygame_gui`, `requests`). En la exposición esto supone un problema:
el ordenador en el que voy a exponer puede no tener Python, o tener una versión diferente.

La solución fue empaquetar el cliente como un ejecutable `.exe` de Windows usando
**PyInstaller** — una herramienta que toma el código Python y lo convierte en un
fichero ejecutable que incluye el intérprete de Python y todas las dependencias
dentro. El resultado es un único `.exe` que cualquier ordenador Windows puede
ejecutar con doble clic, sin instalar nada.

#### ¿Cómo se generó?

```bash
# Instalamos PyInstaller
pip install pyinstaller

# Generamos el ejecutable
pyinstaller --onefile --windowed main.py
```

- `--onefile` — empaqueta todo en un único `.exe` en vez de una carpeta con múltiples ficheros
- `--windowed` — evita que aparezca una ventana de terminal negra al ejecutar el juego

El ejecutable generado aparece en la carpeta `dist/main.exe`.

#### Limitaciones

- El ejecutable generado en Windows solo funciona en Windows. Si se quisiera
  distribuir en Mac o Linux habría que generarlo desde esos sistemas operativos.
- El `config.py` con la `SERVER_URL` queda fijada en el momento de compilar —
  si el servidor cambia de IP hay que recompilar el ejecutable.
