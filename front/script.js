const API_URL = "http://127.0.0.1:5000";

// Логин
function login(event) {
    event.preventDefault(); // чтобы страница не перезагружалась

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message === "Успешный вход") {
            localStorage.setItem("user", email);
            window.location.href = "index.html";
        } else {
            document.getElementById("message").innerText = data.message;
        }
    });
}


// Регистрация
function register() {
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
        if (data.message === "Пользователь зарегистрирован") {
            window.location.href = "login.html";
        } else {
            document.getElementById("message").innerText = data.message;
        }
    });
}

// Выход
function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}
