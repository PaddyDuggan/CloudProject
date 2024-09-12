const express = require('express');
const cors = require('cors'); // Import the cors package
const app = express();
const PORT = process.env.PORT || 3001;

// Use the CORS middleware
app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json());

function classifyIP(ip) {
    if (ip.includes('.')) {
        const parts = ip.split('.');
        if (parts.length === 4) {
            return 'IPv4';
        }
    } else if (ip.includes(':')) {
        const parts = ip.split(':');
        if (parts.length >= 2 && parts.length <= 8) {
            return 'IPv6';
        }
    }
    return 'Unknown';
}

app.post('/classify', (req, res) => {
    const { ips } = req.body;

    // Check if ips is provided and is a non-empty array
    if (!ips || !Array.isArray(ips) || ips.length === 0 || ips.every(ip => ip.trim() === '')) {
        return res.status(400).json({ error: 'Please enter at least one IP address.' });
    }

    const results = ips.map(ip => {
        const classification = classifyIP(ip);
        return `${ip} -> ${classification}`;
    });

    res.json({ results });
});

const server = app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

module.exports = { classifyIP, server };

