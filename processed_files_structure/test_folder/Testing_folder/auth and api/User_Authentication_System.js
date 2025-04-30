/**
 * * Authenticates a user based on the provided username and password.
 *
 * @param {string} username - The username of the user.
 * @param {string} password - The password of the user.
 * @returns {string|null} A JWT token if authentication is successful, otherwise null.
 */
function authenticateUser(username, password) {
    const user = users.find(u => u.username === username && u.password === password);
    if (!user) return null;

    return jwt.sign({ id: user.id, username: user.username }
/**
 * * Middleware to verify the JWT token from the request header.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @param {Function} next - The next middleware function.
 * @returns {Object} Returns a JSON response with an error message if the token is missing.
 */
function verifyToken(req, res, next) {
    const token = req.headers["authorization"];
    if (!token) return res.status(403).json({ message: "Token required" }
