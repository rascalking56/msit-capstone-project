const API_BASE = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

function getRoleFromToken() {
    const token = getToken();
    if (!token) return null;
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role;
}

function applyRoleUI() {
    const role = getRoleFromToken();

    document.querySelectorAll(".admin-only").forEach(el => {
        el.style.display = role === "admin" ? "block" : "none";
    });

    document.querySelectorAll(".staff-only").forEach(el => {
        el.style.display = (role === "staff" || role === "admin") ? "block" : "none";
    });

    document.querySelectorAll(".customer-only").forEach(el => {
        el.style.display = role === "customer" ? "block" : "none";
    });
}

async function apiGet(path) {
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            "Authorization": `Bearer ${getToken()}`,
        },
    });
    return res.json();
}

async function loadUsers() {
    const data = await apiGet("/users/");
    document.getElementById("usersOutput").textContent = JSON.stringify(data, null, 2);
}

async function loadInventory() {
    const data = await apiGet("/inventory/all");
    document.getElementById("inventoryOutput").textContent = JSON.stringify(data, null, 2);
}

async function loadMyOrders() {
    const data = await apiGet("/orders/my");
    document.getElementById("myOrdersOutput").textContent = JSON.stringify(data, null, 2);
}

async function loadLowStock() {
    const data = await apiGet("/alerts/low-stock");
    document.getElementById("alertsOutput").textContent = JSON.stringify(data, null, 2);
}

async function loadAuditLogs() {
    const data = await apiGet("/audit/dashboard");
    document.getElementById("auditOutput").textContent = JSON.stringify(data, null, 2);
}

document.addEventListener("DOMContentLoaded", applyRoleUI);
