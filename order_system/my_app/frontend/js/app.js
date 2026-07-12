const API = "http://127.0.0.1:8000";

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            window.location.href = "dashboard.html";
        } else {
            document.getElementById("login-status").innerText = "Login failed.";
        }
    });
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "login.html";
}

function authHeaders() {
    return {
        "Authorization": "Bearer " + localStorage.getItem("access_token")
    };
}

function loadProducts() {
    fetch(`${API}/products/`, { headers: authHeaders() })
        .then(res => res.json())
        .then(data => {
            document.getElementById("products").innerText = JSON.stringify(data, null, 2);
        });
}

function loadInventory() {
    fetch(`${API}/inventory/all`, { headers: authHeaders() })
        .then(res => res.json())
        .then(data => {
            document.getElementById("inventory").innerText = JSON.stringify(data, null, 2);
        });
}

function loadOrders() {
    fetch(`${API}/orders/`, { headers: authHeaders() })
        .then(res => res.json())
        .then(data => {
            document.getElementById("orders").innerText = JSON.stringify(data, null, 2);
        });
}

function loadAudit() {
    fetch(`${API}/audit/dashboard`, { headers: authHeaders() })
        .then(res => res.json())
        .then(data => {
            document.getElementById("audit").innerText = JSON.stringify(data, null, 2);
        });
}

function loadAlerts() {
    fetch(`${API}/alerts/low-stock`, { headers: authHeaders() })
        .then(res => res.json())
        .then(data => {
            document.getElementById("alerts").innerText = JSON.stringify(data, null, 2);
        });
}
