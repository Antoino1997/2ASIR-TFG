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
