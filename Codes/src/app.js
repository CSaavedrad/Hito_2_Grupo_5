import express from 'express';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import sqlite3 from 'sqlite3';

const app = express();
const port = 3000;

app.use(morgan('dev'));
app.use(bodyParser.json());

const db = new sqlite3.Database('talleres.db');

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS talleres (
        nombre TEXT,
        clases_de TEXT,
        locacion TEXT,
        precio TEXT,
        contacto TEXT PRIMARY KEY,
        validado INTEGER DEFAULT 0
    )`);
});

app.post('/busqueda', (req, res) => {
    const userInput = req.body.description;

    const pythonProcess = spawn('python', ['Sistema-de-busqueda-POO.py', userInput], { encoding: 'utf8' });
    
    let accumulatedData = '';

    pythonProcess.stdout.on('data', (data) => {
        const dataString = data.toString();
        accumulatedData += dataString;
        if (dataString.includes('<<end_of_data>>')) {
            try {
                const jsonData = JSON.parse(accumulatedData.replace('<<end_of_data>>', ''));

                db.get('SELECT COUNT(*) AS count FROM talleres WHERE contacto = ?', [jsonData[1].Contacto], (err, row) => {
                    if (err) {
                        console.error('Error verificando el contacto en la base de datos:', err);
                        res.status(500).json({ error: 'Internal Server Error' });
                        return;
                    }

                    if (row.count > 0) {
                        res.status(400).json({ error: 'El contacto ya está registrado en la base de datos' });
                        return;
                    }

                    const stmt = db.prepare('INSERT INTO talleres VALUES (?, ?, ?, ?, ?, ?)');
                    jsonData.forEach((entry) => {
                        if (typeof entry === 'object') {
                            const values = [
                                entry.Nombre,
                                entry["Clases de"],
                                entry.Locacion,
                                entry.Precio,
                                entry.Contacto,
                                0
                            ];
                            stmt.run(values);
                        }
                    });
                    stmt.finalize();

                    res.json(jsonData);
                });
            } catch (error) {
                console.error('Error parsing JSON:', error);
                res.status(500).json({ error: 'Internal Server Error' });
            }

            accumulatedData = '';
        }
    });
});

app.get('/imprimir_basededatos', (req, res) => {
    db.all('SELECT * FROM talleres', (err, rows) => {
        if (err) {
            console.error('Error al obtener los datos de la base de datos:', err);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }

        res.json(rows);
    });
});

app.post('/marcar_contactado', (req, res) => {
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


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
