/**
 * * Fetches user data from the API.
 *
 * @async
 * @returns {Promise} A promise that resolves with the user data if the fetch is successful.
 * @throws {Error} If the fetch fails or the response is not ok.
 */
function fetchUserData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}
function filterUsersByCity(users, city) {
    return users.filter(user => user.address.city === city);
}
/**
 * * Displays user information to the console.
 *
 * @param {Array} users - An array of user objects, where each object has a 'name' property.
 */
function displayUsers(users) {
    users.forEach(user => {
        console.log(`Name: ${user.name}
