import express from 'express';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';

const app = express();
const port = 3000;

// Middleware
app.use(morgan('dev'));
app.use(bodyParser.json());

// Endpoint for processing user input
app.post('/process-input', (req, res) => {
    const userInput = req.body.description;

    // Execute the Python script with the user input
    const pythonProcess = spawn('python', ['scrapePOO.py', userInput]);

    pythonProcess.stdout.on('data', (data) => {
        // Parse the JSON response
        const jsonOutput = JSON.parse(data.toString());
        
        // Send the JSON response
        res.json(jsonOutput);
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});