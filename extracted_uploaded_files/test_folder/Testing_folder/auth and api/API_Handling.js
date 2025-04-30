const API_URL = "https://jsonplaceholder.typicode.com/users";

async function fetchUserData() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching data:", error);
        return [];
    }
}

function filterUsersByCity(users, city) {
    return users.filter(user => user.address.city === city);
}

function displayUsers(users) {
    users.forEach(user => {
        console.log(`Name: ${user.name}, Email: ${user.email}, City: ${user.address.city}`);
    });
}

// Example usage
fetchUserData().then(users => {
    const nyUsers = filterUsersByCity(users, "New York");
    console.log("Users in New York:");
    displayUsers(nyUsers);
});
