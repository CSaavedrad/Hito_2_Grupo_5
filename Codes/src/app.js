import express from 'express';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import sqlite3 from 'sqlite3';
import { v4 as uuidv4 } from 'uuid';

const app = express();
const port = 3000;

// Middleware
app.use(morgan('dev'));
app.use(bodyParser.json());

// Crear la conexión a la base de datos SQLite
const db = new sqlite3.Database('talleres.db');

// Crear la tabla 'talleres' si no existe
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS talleres (
        nombre TEXT,
        clases_de TEXT,
        locacion TEXT,
        precio TEXT,
        contacto TEXT PRIMARY KEY,
        validado INTEGER DEFAULT 0,
        propuesta TEXT DEFAULT "Genere un link de contacto"
    )`);
});

// Endpoint
// Endpoint
app.post('/busqueda', (req, res) => {
    const userInput = req.body.description;

    const pythonProcess = spawn('python', ['Sistema-de-busqueda-POO.py', userInput], { encoding: 'utf8' });
    
    let accumulatedData = '';

    pythonProcess.stdout.on('data', (data) => {
        const dataString = data.toString();

        // Accumulate data until the delimiter is found
        accumulatedData += dataString;

        try {
            // Remove the delimiter and parse JSON
            const jsonData = JSON.parse(accumulatedData.replace('<<end_of_data>>', ''));

            if (jsonData.message) {
                res.json(jsonData);
                return;
            }

            // Preparar la sentencia REPLACE INTO
            const stmt = db.prepare('REPLACE INTO talleres (nombre, clases_de, locacion, precio, contacto, validado, propuesta) VALUES (?, ?, ?, ?, ?, ?, ?)');

            // Ejecutar la inserción/reemplazo para cada entrada en jsonData
            jsonData.forEach((entry) => {
                if (typeof entry === 'object') {
                    const values = [
                        entry.Nombre,
                        entry["Clases de"],
                        entry.Locacion,
                        entry.Precio,
                        entry.Contacto,
                        0,
                        "Genere un link de contacto"
                    ];
                    stmt.run(values, (err) => {
                        if (err) {
                            console.error('Error insertando el registro en la base de datos:', err);
                            res.status(500).json({ error: 'Internal Server Error' });
                        }
                    });
                }
            });

            stmt.finalize((err) => {
                if (err) {
                    console.error('Error finalizando la sentencia:', err);
                    res.status(500).json({ error: 'Internal Server Error' });
                } else {
                    // Enviar los datos al cliente
                    res.json(jsonData);
                }
            });
        } catch (error) {
            console.error('Error parsing JSON:', error);
            res.status(500).json({ error: 'Internal Server Error' });
        }

        // Reset accumulated data
        accumulatedData = '';
    });
});


// Agregar una nueva ruta para mostrar el historial
app.get('/historial', (req, res) => {
    // Realizar una consulta a la base de datos para obtener todos los registros
    db.all('SELECT * FROM talleres', (err, rows) => {
        if (err) {
            console.error('Error al obtener los datos de la base de datos:', err);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }

        if(rows.length === 0){
            res.json("El historial está vacío");
            return;
        }

        // Enviar los datos de la base de datos al cliente
        res.json(rows);
    });
});

// Nueva ruta para marcar un contacto como validado
app.post('/marcar_validado', (req, res) => {
    const { contacto, validado } = req.body;

    db.run('UPDATE talleres SET validado = ? WHERE contacto = ?', [validado ? 1 : 0, contacto], (err) => {
        if (err) {
            console.error('Error al actualizar el estado de validado en la base de datos:', err);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }

        res.json({ success: true });
    });
});

// Nueva ruta para generar un enlace
app.post('/generar_enlace', (req, res) => {

    const { contacto } = req.body;
    const token = uuidv4();
    const enlace = `http://localhost:8501/?token=${token}`;

    db.run('UPDATE talleres SET propuesta = ? WHERE contacto = ?', [enlace, contacto], (err) => {
        if (err) {
            console.error('Error al actualizar el estado de validado en la base de datos:', err);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }

        res.json({ success: true });
    });
});


// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
