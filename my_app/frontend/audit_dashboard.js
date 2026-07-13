const API = "http://127.0.0.1:8000";

function token() {
    return localStorage.getItem("access_token");
}

async function api(path) {
    const res = await fetch(`${API}${path}`, {
        headers: { "Authorization": `Bearer ${token()}` }
    });
    return res.json();
}

async function applyFilters() {
    const user = document.getElementById("filterUser").value;
    const action = document.getElementById("filterAction").value;
    const start = document.getElementById("filterStart").value;
    const end = document.getElementById("filterEnd").value;

    const params = new URLSearchParams({
        user,
        action,
        start,
        end
    });

    const data = await api(`/audit/analytics/filter?${params.toString()}`);
    document.getElementById("auditOutput").textContent = JSON.stringify(data, null, 2);

    const suspicious = await api("/audit/analytics/suspicious");
    document.getElementById("suspiciousOutput").textContent = JSON.stringify(suspicious, null, 2);
}

function exportCSV() {
    window.location = `${API}/audit/analytics/export/csv`;
}

function exportJSON() {
    window.location = `${API}/audit/analytics/export/json`;
}

document.addEventListener("DOMContentLoaded", applyFilters);
