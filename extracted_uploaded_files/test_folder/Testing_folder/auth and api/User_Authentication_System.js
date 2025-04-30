const express = require("express");
const jwt = require("jsonwebtoken");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

const SECRET_KEY = "your_secret_key"; // Replace with an actual secure key

const users = [
    { id: 1, username: "admin", password: "password123" },
    { id: 2, username: "user", password: "mypassword" }
];

function authenticateUser(username, password) {
    const user = users.find(u => u.username === username && u.password === password);
    if (!user) return null;

    return jwt.sign({ id: user.id, username: user.username }, SECRET_KEY, { expiresIn: "1h" });
}

function verifyToken(req, res, next) {
    const token = req.headers["authorization"];
    if (!token) return res.status(403).json({ message: "Token required" });

    jwt.verify(token.split(" ")[1], SECRET_KEY, (err, decoded) => {
        if (err) return res.status(401).json({ message: "Invalid token" });
        req.user = decoded;
        next();
    });
}

// Routes
app.post("/login", (req, res) => {
    const { username, password } = req.body;
    const token = authenticateUser(username, password);

    if (!token) return res.status(401).json({ message: "Invalid credentials" });
    res.json({ token });
});

app.get("/protected", verifyToken, (req, res) => {
    res.json({ message: "Access granted!", user: req.user });
});

// Start server
app.listen(3000, () => console.log("Server running on port 3000"));
