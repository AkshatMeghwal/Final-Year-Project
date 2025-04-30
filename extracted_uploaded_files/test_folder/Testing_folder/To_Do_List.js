const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

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

function removeTask(taskElement) {
    taskElement.remove();
    saveTasks();
}

function saveTasks() {
    const tasks = Array.from(todoList.children).map(li => li.textContent);
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function loadTasks() {
    const storedTasks = JSON.parse(localStorage.getItem("tasks")) || [];
    storedTasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task;
        li.onclick = () => removeTask(li);
        todoList.appendChild(li);
    });
}

document.addEventListener("DOMContentLoaded", loadTasks);
