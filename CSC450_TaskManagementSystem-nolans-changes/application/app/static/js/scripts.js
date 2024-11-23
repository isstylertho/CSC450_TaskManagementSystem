document.addEventListener("DOMContentLoaded", function () {
    // Initialize FullCalendar
    var calendarEl = document.getElementById("calendar");
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: "/tasks", // Fetch tasks from the server
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
        },
        dateClick: function (info) {
            openTaskModal(null, info.dateStr);
        },
        eventClick: function (info) {
            const event = info.event;
            openTaskModal(event.id, event.startStr, event.title, event.extendedProps.description);
        }
    });
    calendar.render();

    // Modal handling
    const modal = document.getElementById("taskModal");
    const closeModal = document.querySelector(".close");
    const taskForm = document.getElementById("taskForm");

    closeModal.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    document.getElementById("addTaskBtn").addEventListener("click", () => {
        openTaskModal();
    });

    function openTaskModal(id = null, date = null, title = "", description = "") {
        document.getElementById("taskId").value = id || "";
        document.getElementById("title").value = title;
        document.getElementById("description").value = description;
        document.getElementById("due_date").value = date || "";
        modal.style.display = "block";
    }

    // Submit task form
    taskForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const formData = new FormData(taskForm);
        const taskId = formData.get("task_id");

        const data = {
            title: formData.get("title"),
            description: formData.get("description"),
            due_date: formData.get("due_date"),
        };

        const method = taskId ? "PUT" : "POST";
        const endpoint = taskId ? `/tasks/${taskId}` : "/tasks";

        const response = await fetch(endpoint, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            modal.style.display = "none";
            calendar.refetchEvents();
        }
    });
});
