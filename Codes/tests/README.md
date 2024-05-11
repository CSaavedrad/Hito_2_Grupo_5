Resultados de las pruebas:

Test1-b.jpg son los resultados al ejecutar las pruebas con la base de datos vacía y Test1-a.jpg y Test1-c cuando tiene datos.

Podemos ver que el segundo Test falla cuando tiene datos que es el comportamiento esperado.

El segundo test tabién falla cuando no hay datos, esto se debe a que aunque la lista si es una lista vacía, no responde la situación de manera adecuada al usuario.

Se encontró un error al realizar la cuarta prueba, cuando la API de open ai no encuentra una temática encontramos un internal server error, esto es ya que intenta agregar a la base de datos los resultados de la búsqueda incluso cuando la búsqueda falla. 

También cabe resaltar que si se realiza la misma búsqueda dos o más veces, hay un exemption dado que el tallerista ya estaba en la base de datos, lo cual provoca
un error para la tercera prueba. Esto se puede ver en Test1-c.