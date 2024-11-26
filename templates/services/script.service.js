document.addEventListener("DOMContentLoaded", () => {
    fetchTasks();

    document.getElementById("addTaskButton").addEventListener("click", addTask);
});

function fetchTasks() {
    fetch("http://localhost:5000/tasks")
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";
            tasks.forEach(task => {
                const taskItem = createTaskElement(task);
                taskList.appendChild(taskItem);
            });
        })
        .catch(error => console.error("Error fetching tasks:", error));
}

function createTaskElement(task) {
    const taskItem = document.createElement("li");
    taskItem.classList.add("task-item");
    taskItem.textContent = task.title;
    if (task.completed) {
        taskItem.classList.add("completed");
    }
    
    taskItem.addEventListener("click", () => {
        toggleTask(task.id, !task.completed);
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteTask(task.id);
    });

    taskItem.appendChild(deleteButton);
    return taskItem;
}

function addTask() {
    const taskInput = document.getElementById("taskInput");
    const title = taskInput.value.trim();

    if (title === "") {
        alert("Task title cannot be empty!");
        return;
    }

    fetch("http://localhost:5000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title })
    })
    .then(response => {
        if (response.ok) {
            fetchTasks();
            taskInput.value = "";
        } else {
            console.error("Error adding task");
        }
    })
    .catch(error => console.error("Error:", error));
}

function toggleTask(id, completed) {
    fetch(`http://localhost:5000/tasks/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ completed })
    })
    .then(response => {
        if (response.ok) {
            fetchTasks();
        } else {
            console.error("Error updating task");
        }
    })
    .catch(error => console.error("Error:", error));
}

function deleteTask(id) {
    fetch(`http://localhost:5000/tasks/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            fetchTasks();
        } else {
            console.error("Error deleting task");
        }
    })
    .catch(error => console.error("Error:", error));
}
