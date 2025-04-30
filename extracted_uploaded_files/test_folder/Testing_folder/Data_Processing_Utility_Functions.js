function formatJSON(jsonString) {
    try {
        const parsed = JSON.parse(jsonString);
        return JSON.stringify(parsed, null, 4);
    } catch (error) {
        console.error("Invalid JSON:", error.message);
        return null;
    }
}

function isValidJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return true;
    } catch {
        return false;
    }
}
function extractKeys(jsonObject, keys) {
    return keys.reduce((acc, key) => {
        if (jsonObject.hasOwnProperty(key)) {
            acc[key] = jsonObject[key];
        }
        return acc;
    }, {});
}

const rawJson = '{"name":"John", "age":30, "city":"New York"}';
console.log("Formatted JSON:\n", formatJSON(rawJson));
console.log("Is valid JSON?", isValidJSON(rawJson));
console.log("Extracted keys:", extractKeys(JSON.parse(rawJson), ["name", "city"]));
