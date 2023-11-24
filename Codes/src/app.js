import express from 'express';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';

const app = express();
const port = 3000;

// Middleware
app.use(morgan('dev'));
app.use(bodyParser.json());

// Endpoint
app.post('/busqueda', (req, res) => {
    const userInput = req.body.description;

    const pythonProcess = spawn('python', ['Sistema-de-busqueda-POO.py', userInput], { encoding: 'utf8' });

    pythonProcess.stdout.on('data', (data) => {
        const jsonOutput = JSON.parse(data.toString());
        res.json(jsonOutput);
    });
});

// Server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});