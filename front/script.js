const API_URL = "http://127.0.0.1:5000";

// ЛОГИН
function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "index.html";
        } else {
            document.getElementById("message").innerText = "Ошибка входа";
        }
    });
}

// РЕГИСТРАЦИЯ
function register(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message === "Регистрация успешна") {
            window.location.href = "login.html";
        } else {
            document.getElementById("message").innerText = data.message;
        }
    });
}

// ВЫХОД
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
