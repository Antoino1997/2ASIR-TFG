<div align="center">
  <h1>TFG - Antonio Pérez Galán</h1>
  <p>Desarrollo de un videojuego en red con Python, Flask y Docker</p>
</div>

## Índice
- [Introducción](#introducción)
- [Arquitectura y Tecnologías Usadas](#arquitectura-y-tecnologías-usadas)
- [Explicación Tecnologías y Alternativas](#explicación-tecnologías-y-alternativas)

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
