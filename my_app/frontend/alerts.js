const API = "http://127.0.0.1:8000";

function token() {
    return localStorage.getItem("access_token");
}

async function api(path, method = "POST", body = {}) {
    const res = await fetch(`${API}${path}`, {
        method,
        headers: {
            "Authorization": `Bearer ${token()}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });
    return res.json();
}

async function runAlerts() {
    const data = await api("/alerts/run");
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

async function sendCritical() {
    const msg = document.getElementById("criticalMsg").value;
    const data = await api("/alerts/critical", "POST", { message: msg });
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}
