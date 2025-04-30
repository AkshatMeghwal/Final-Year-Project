/**
 * * Formats a JSON string into a human-readable format with indentation.
 *
 * @param {string} jsonString - The JSON string to format.
 * @returns {string} The formatted JSON string with indentation, or the original string if parsing fails.
 */
function formatJSON(jsonString) {
    try {
        const parsed = JSON.parse(jsonString);
        return JSON.stringify(parsed, null, 4);
    }
function isValidJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return true;
    }
/**
 * * Extracts specific keys from a JSON object into a new object.
 *
 * @param {object} jsonObject - The JSON object to extract keys from.
 * @param {string[]} keys - An array of keys to extract from the JSON object.
 * @returns {object} A new object containing only the specified keys and their values from the original JSON object.
 */
function extractKeys(jsonObject, keys) {
    return keys.reduce((acc, key) => {
        if (jsonObject.hasOwnProperty(key)) {
            acc[key] = jsonObject[key];
        }
