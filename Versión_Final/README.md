<div align="center">
  <h1>TFG - Antonio Pérez Galán</h1>
  <p>Desarrollo de un videojuego en red con Python, Flask y Docker</p>
</div>

## Índice
- [Introducción](#introducción)
- [Arquitectura y Tecnologías Usadas](#arquitectura-y-tecnologías-usadas)
- [Tecnologías Alternativas](#tecnologías-alternativas)

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

## Tecnologías Alternativas
