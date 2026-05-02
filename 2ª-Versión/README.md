Segunda versión que contiene la parte del servidor. Aunque he hecho más cambios a lo largo del TFG, está se podría considerar la versión final del servidor.
Contiene los API points para que el cliente se pueda comunicar y mostrar la información, la página web que muestra el ranking y además esta dockerizado. Simplemente hay que montar la imagen y crear el contenedor.

Para montar la imagen, hacemos:
~~~
docker build -t nombre_imagen .
~~~

Para crear el contenedor, hacemos:
~~~
docker compose up
~~~

Como yo estoy descargando la imagen desde mi repositorio de docker hub, solo tengo que hacer el segundo comando.
