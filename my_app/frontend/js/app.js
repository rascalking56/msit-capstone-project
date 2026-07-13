function getRoleFromToken() {
    const token = localStorage.getItem("access_token");
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

document.addEventListener("DOMContentLoaded", applyRoleUI);
