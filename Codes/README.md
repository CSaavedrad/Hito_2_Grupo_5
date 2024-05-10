Es importante instalar las librerías necesarias (selenium, beautifulsoup4, request, openai, unicodedata 
y streamlit), recomendado el uso de pip,
también es necesario tener instalado google Chrome y seguir los pasos de la documentación de openai.
https://platform.openai.com/docs/quickstart?context=python

Para correr la API es necesario abrir un terminal en la carpeta codes, luego realizar el comando "npm install"
Luego cada vez que se quiera utilizar el sistema es necesario poner el comando "npm run dev" para correr la API
y "streamlit run Interfaz.py" o "python3 -m streamlit run Interfaz.py" para correr la interfaz, que se abrirá en Chrome.

También es necesario node.js y quizás otras cosas que teniamos instaladas de antes.

Los programas fueron programados y testeados en Python 3.11.2

## A partir de Hito 2 - Ingeniería de Software 2024-1

### Requisitos:

* Instalar SQlite3: npm install sqlite3
* Installar uuidv4: npm install uuidv4

### Cambios en el código:

* La función WebScrapper del sistema de búsqueda fue actualizada para adecuarse a los cambios de formato de la página tusprofesoresparticulares.cl de donde sacamos información

* app.js Ahora crea la base de datos talleres.db en la que se guarda el historial de búsquedas. También gestiona la conexión entre la interfaz y la base de datos con nuevos endpoints.

* Interfaz.py Crea un apartado en la página para que se pueda ver la base de datos. En ese apartado es posible marcar si un tallerista ha sido contactado o no.
