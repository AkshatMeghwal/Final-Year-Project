/**
 * * Adds a new task to the todo list.
 *
 * This function takes the value from the todo input field, creates a new list item,
 * adds it to the todo list, and saves the updated list to local storage. It also
 * clears the input field after adding the task.
 *
 * @returns {void}
 */
function addTask() {
    const task = todoInput.value.trim();
    if (task === "") return;

    const li = document.createElement("li");
    li.textContent = task;
    li.onclick = () => removeTask(li);
    todoList.appendChild(li);

    saveTasks();
    todoInput.value = "";
}
/**
 * * Removes a task element from the todo list and updates local storage.
 *
 * @param {HTMLElement} taskElement - The HTML element representing the task to be removed.
 * @returns {void}
 */
function removeTask(taskElement) {
    taskElement.remove();
    saveTasks();
}
/**
 * * Saves the current tasks in the todo list to local storage.
 *
 * The function retrieves all task items from the todo list, extracts their text content,
 * and saves them as a JSON string in the local storage under the key "tasks".
 *
 * @returns {void}
 */
function saveTasks() {
    const tasks = Array.from(todoList.children).map(li => li.textContent);
    localStorage.setItem("tasks", JSON.stringify(tasks));
}
/**
 * * Loads tasks from local storage and displays them in the todo list.
 *
 * @returns {void}
 */
function loadTasks() {
    const storedTasks = JSON.parse(localStorage.getItem("tasks")) || [];
    storedTasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task;
        li.onclick = () => removeTask(li);
        todoList.appendChild(li);
    }
